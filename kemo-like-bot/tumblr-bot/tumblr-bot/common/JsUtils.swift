//
//  JsUtils.swift
//  tumblr-bot
//
//  Created by Michal Racek on 05/09/16.
//  Copyright © 2016 PyJunkies. All rights reserved.
//

import Cocoa
import Foundation
import WebKit


enum JsFunctionError: Error {
	case ScriptLoading(message: String)
	case ElementNotFound(message: String)
}

// Swift binding to javascript 'jsPageApi' module defined by 'page.base.js'
public class JsPageApi {
	
	let webView: WebView
	
	public init(webView: WebView){
		self.webView = webView
	}
	
	public func async(execFn: @escaping (JsPageApi)->Void)->AsyncChain<JsPageApi> {
		return AsyncChain<JsPageApi>(execFn: execFn, param: self)
	}
	
	@discardableResult public func exists(selector: String)->Bool{
		let res = withJsPageApiRun(script: "jsPageApi.exists(\"\(selector)\")")
		return res == "true"
	}
	
	@discardableResult public func setValueOf(selector: String, value: String)->PageApiResult{
		let res = withJsPageApiRun(script: "jsPageApi.setValueTo(\"\(selector)\",\"\(value)\")")
		return PageApiResult.toResult(jsResult:res, errorMessage: { return "Setting value using selector \(selector) failed!"})
	}
	
	@discardableResult public func submit(selector: String)->PageApiResult{
		let res = withJsPageApiRun(script: "jsPageApi.submit(\"\(selector)\")")
		return PageApiResult.toResult(jsResult:res, errorMessage: { return "Form submit using selector \(selector) failed!"})
	}
	
	@discardableResult public func clickOn(selector: String)->PageApiResult{
		let res = withJsPageApiRun(script: "jsPageApi.clickOn(\"\(selector)\")")
		return PageApiResult.toResult(jsResult:res, errorMessage: { return "Clicking on element using selector \(selector) failed!"})
	}
	
	@discardableResult public func waitThen(selector: String, onFind: @escaping (String, WebView)->Void)->PageApiResult{
		// Ask page for element
		var res = withJsPageApiRun(script: "jsPageApi.exists(\"\(selector)\")")
		var attempts = 0;
		// Try asking for element few times with delay
		while(res != "true" && attempts < 15){
			DispatchQueue.global(qos: DispatchQoS.QoSClass.background).sync {
				res = withJsPageApiRun(script: "jsPageApi.exists(\"\(selector)\")")
				attempts+=1;
			}
			sleep(1)
		}
		if(res == "false"){
			return PageApiResult.toResult(jsResult: res, errorMessage: { return "Cannot find element using selector \(selector) for \(attempts) times!"})
		}else{
			onFind(selector, webView)
			return PageApiResult.toResult(jsResult: "Element was found and action exectuted using selector \(selector).")
		}
	}
	
	public func isJsPageApiLoaded()->Bool{
		let res: String? = webView.stringByEvaluatingJavaScript(from: "typeof(jsPageApi) !== 'undefined' ? 'true' : 'false'")
		return res == "true"
	}
	
	private func withJsPageApiRun(script: String)->String{
		var	scriptRes = ""
		DispatchQueue.main.sync {
			// Init page JS Page api only when needed
			if(!isJsPageApiLoaded()){
				// Load page base script data
				let path = Bundle.main.path(forResource: "page.base", ofType: "js")
				let data = try! String(contentsOf: URL(fileURLWithPath:path!))
				// Execute loaded script on given webView
				webView.stringByEvaluatingJavaScript(from: data)
			}
			// Run required script
			scriptRes = webView.stringByEvaluatingJavaScript(from: script)!
		}
		return scriptRes
	}
	
}

// Represents result of performed JsPageApi
public struct PageApiResult {
	let ok: Bool
	let message: String
	
	static func toResult(jsResult: String, errorMessage: ()->String)->PageApiResult{
		if jsResult == "" || jsResult == "false" {
			return PageApiResult(ok: false, message: errorMessage())
		}
		return PageApiResult(ok: true, message: jsResult)
	}
	
	static func toResult(jsResult: String)->PageApiResult{
		if jsResult == "" || jsResult == "false" {
			return PageApiResult(ok: false, message: "No error message available.")
		}
		return PageApiResult(ok: true, message: jsResult)
	}
}



