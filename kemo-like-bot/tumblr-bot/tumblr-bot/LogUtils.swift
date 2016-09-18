//
//  LogUtils.swift
//  tumblr-bot
//
//  Created by Michal Racek on 04/09/16.
//  Copyright © 2016 PyJunkies. All rights reserved.
//

import Foundation
import Cocoa


public class LogView {
	
	let textView:NSTextView
	
	let infoAttrs: [String: AnyObject] = [
		NSForegroundColorAttributeName: NSColor.black
	]
	
	let errorAttrs: [String: AnyObject] = [
		NSForegroundColorAttributeName: NSColor.red
	]
	
	let okAttrs: [String: AnyObject] = [
		NSForegroundColorAttributeName: NSColor.blue
	]
	
	public init(textView: NSTextView){
		self.textView = textView
	}
	
	public func info(msg: String){
		DispatchQueue.main.async {
			self.textView.textStorage?.append(NSMutableAttributedString(string: "\n\(msg)", attributes: self.infoAttrs))
			self.textView.display()
		}
	}
	
	public func ok(msg: String){
		DispatchQueue.main.async {
			self.textView.textStorage?.append(NSMutableAttributedString(string: "\n\(msg)", attributes: self.okAttrs))
			self.textView.display()
		}
	}
	
	public func error(msg: String){
		DispatchQueue.main.async {
			self.textView.textStorage?.append(NSMutableAttributedString(string: "\n\(msg)", attributes: self.errorAttrs))
			self.textView.display()
		}
	}
	
}
