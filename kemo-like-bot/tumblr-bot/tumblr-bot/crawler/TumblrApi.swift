//
//  TumblrApi.swift
//  tumblr-bot
//
//  Created by Michal Racek on 10/09/16.
//  Copyright © 2016 PyJunkies. All rights reserved.
//

import Foundation

// Provides basic api over Tumblr web
public class TumblrApi {
	
	// Basic web page api
	let webApi: WebApi
	// Page JS api
	let jsPageApi: JsPageApi
	// UI logging component
	let logView: LogView
	
	public init(webApi: WebApi, logView: LogView){
		self.webApi = webApi
		self.logView = logView
		self.jsPageApi = JsPageApi(webView: self.webApi.webView)
	}
	
	public func login(login: String, password: String)->Task<Bool>{
		let task = Task<Bool>(name: "login")
		task.plan {
			self.isLoggedIn().run(onComplete: { isLogged in
				if isLogged {
					self.logView.info(msg:"🖥We are already logged in. Skipping.")
					// Call result handler that we are already logged in
					task.complete(result: true)
				}else{
					task.plan {
						self.logView.info(msg:"Conecting to tumblr web 🕔")
						// Logout first then go back to login and run login scripts
						self.webApi.load(url: "https://www.tumblr.com/logout", then: {webView in
							self.logView.info(msg:"🖥Tumblr logout page loaded")
						}).then(url: "https://www.tumblr.com/login", then: {webView in
							self.logView.info(msg:"🖥Tumblr login page loaded")
							// Run login scripts
							self.fillLoginForm(login: login, password: password)
								.then(execFn: { jsPageApi in
									// Call result handler that we are logged in
									task.complete(result: true)
								})
								.run()
						}).load()
					}
				}
			})
		}
		return task
	}
	
	public func isLoggedIn()->Task<Bool>{
		let task = Task<Bool>(name: "isLoggedIn")
		task.plan {
			self.jsPageApi.async(execFn: {jsPageApi in
				jsPageApi.waitThen(selector: ".icon_user_settings", onFind: { selector, webView in
					
				})
				let exists = jsPageApi.exists(selector: ".icon_user_settings")
				task.complete(result: exists)
			}).run()
		}
		return task
	}
	
	func fillLoginForm(login: String, password: String)->AsyncChain<JsPageApi>{
		return jsPageApi.async(execFn: {jsPageApi in
			self.logView.info(msg:"🤖Running login scripts")
			jsPageApi.waitThen(selector: "#signup_determine_email", onFind: { selector, webView in
				// Fill login
				jsPageApi.setValueOf(selector: "#signup_determine_email", value: login)
				jsPageApi.clickOn(selector: "#signup_forms_submit")
				// Fill password
				jsPageApi.setValueOf(selector: "#signup_password", value: password)
			})
		}).then(execFn: {jsPageApi in
			// Wait for login button and click
			let loginClickResult = jsPageApi.waitThen(selector: "span.signup_login_btn.active", onFind: { selector, webView in
				self.logView.info(msg:"Login button found")
				if jsPageApi.clickOn(selector: "span.signup_login_btn.active").ok {
					self.logView.info(msg:"Login button clicked")
				}
			})
			self.logResult(of: loginClickResult)
			// Check that we are logged in
			jsPageApi.waitThen(selector: ".icon_user_settings", onFind: { selector, webView in
				self.logView.ok(msg:"🎉We are logged in!🎉")
			})
		}).then(execFn: {jsPageApi in
			self.logView.info(msg:"🤖Login scripts done")
		})
	}
	
	func search(term: String)->AsyncChain<JsPageApi>{
		return jsPageApi.async(execFn:{jsPageApi in
			self.logView.info(msg:"🤖Running search scripts")
			jsPageApi.waitThen(selector: "#search_query", onFind: { selector, webView in
				// Fill search query
				jsPageApi.setValueOf(selector: "#search_query", value: term)
				// Submit search form
				jsPageApi.submit(selector: "#search_form")
			})
		})
	}
	
	func logResult(of: PageApiResult){
		if of.ok {
			self.logView.info(msg:of.message)
		}else{
			self.logView.error(msg:of.message)
		}
	}
	
	
	
}
