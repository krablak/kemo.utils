//
//  TumblrCrawler.swift
//  tumblr-bot
//
//  Created by Michal Racek on 04/09/16.
//  Copyright © 2016 PyJunkies. All rights reserved.
//

import Foundation


public class TumblrWebCrawler {
	
	// Basic web page api
	let webApi: WebApi
	// Page JS api
	let jsPageApi: JsPageApi
	// UI logging component
	let logView: LogView
	// Tumblr api
	let tumblrApi: TumblrApi
	
	public init(webApi: WebApi, logView: LogView){
		self.webApi = webApi
		self.logView = logView
		self.jsPageApi = JsPageApi(webView: self.webApi.webView)
		self.tumblrApi = TumblrApi(webApi:  webApi, logView: logView)
	}
	
	public func likeThemAll(){
		self.tumblrApi.login(login: "team@kemo.rocks", password: "qfVuF8mu3Y").run(onComplete: {loggedIn in
			debugPrint("We are logged in: \(loggedIn)")
		}).run(onComplete: { loggedIn in
			debugPrint("We are logged in 2: \(loggedIn)")
		})
	}
	
}
