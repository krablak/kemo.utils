//
//  WebUtils.swift
//  tumblr-bot
//
//  Created by Michal Racek on 04/09/16.
//  Copyright © 2016 PyJunkies. All rights reserved.
//

import Foundation
import WebKit

public class WebApi : NSObject, WebFrameLoadDelegate {
	
	let webView: WebView
	
	var onLoadFn: (WebApi)->Void = {webApi in }
	
	public init(webView: WebView) {
		self.webView = webView
		super.init()
		self.webView.frameLoadDelegate = self
	}
	
	public func load(url: String, then: @escaping (WebView)->Void) -> LoadChain {
		return LoadChain(webView: self.webView, url: url, then: then)
	}
	
}

// Helper for chaining web page loads calls
public class LoadChain : NSObject, WebFrameLoadDelegate {
	
	let webView: WebView
	
	// Reference to first part of chain
	private var first: LoadChain?
	
	// Reference to next part of chain
	private var next: LoadChain?
	
	// Planned request
	var request: URLRequest?
	
	// Action executed on page load
	let onLoad: (WebView)->Void
	
	init(webView: WebView, url: String, then: @escaping (WebView)->Void) {
		self.webView = webView
		self.request = URLRequest(url: URL(string: url)!)
		self.onLoad = then
		super.init()
		self.first = self
	}
	
	private init(webView: WebView, first: LoadChain, url: String ,then: @escaping (WebView)->Void) {
		self.webView = webView
		self.first = first
		self.request = URLRequest(url: URL(string: url)!)
		self.onLoad = then
	}
	
	// Plan next page load
	@discardableResult public func then(url: String, then: @escaping (WebView)->Void) -> LoadChain {
		// Create chain next part
		let nextPart = LoadChain(webView: self.webView, first: self.first!, url: url, then: then)
		// Set referece to current part
		self.next = nextPart
		// Return next part as result for further chaining
		return nextPart
	}
	
	// Run planned page loads
	public func load(){
		DispatchQueue.main.async {
			self.webView.frameLoadDelegate = self.first!
			self.first!.webView.mainFrame.load(self.first!.request!)
		}
	}
	
	// WebFrameLoadDelegate called on load page
	public func webView(_ sender: WebView!, didFinishLoadFor frame: WebFrame!){
		// Handle only main frame load events
		if self.webView.mainFrame == frame {
			DispatchQueue.main.async {
				// Execute curren on load action
				self.onLoad(self.webView)
				if self.next != nil && self.next!.request != nil {
					// Start next page load
					let nextPart = self.next!
					self.webView.frameLoadDelegate = nextPart
					self.first!.webView.mainFrame.load(nextPart.request!)
				}else{
					self.webView.frameLoadDelegate = nil
				}
			}
		}
	}
	
}
