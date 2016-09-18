//
//  ViewController.swift
//  tumblr-bot
//
//  Created by Michal Racek on 04/09/16.
//  Copyright © 2016 PyJunkies. All rights reserved.
//

import Cocoa
import WebKit

class ViewController: NSViewController {
	
	@IBOutlet weak var webView: WebView!
	
	@IBOutlet var logTextView: NSTextView!
	
	lazy var webApi : WebApi = {
		return WebApi(webView: self.webView)
	}()
	
	lazy var logView : LogView = {
		return LogView(textView: self.logTextView)
	}()
	
	lazy var tumblrWebCrawler: TumblrWebCrawler = {
		return TumblrWebCrawler(webApi: self.webApi,logView: self.logView)
	}()
	
	override func viewDidLoad() {
		super.viewDidLoad()
		self.logView.ok(msg:"🚀Tumblr Bot Started 🚀")
		self.tumblrWebCrawler.likeThemAll()
	}
	
	override var representedObject: Any? {
		didSet {
			// Update the view, if already loaded.
		}
	}
	
	
}

