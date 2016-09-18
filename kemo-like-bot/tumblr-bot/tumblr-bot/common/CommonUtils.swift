//
//  CommonUtils.swift
//  tumblr-bot
//
//  Created by Michal Racek on 10/09/16.
//  Copyright © 2016 PyJunkies. All rights reserved.
//

import Foundation

// Represents asynchronous task with result
public class Task<T> {
	
	private var name = "unknown"
	
	private var action: ()->Void
	
	private var onComplete: (T)->Void
	
	public init(){
		self.action = {_ in }
		self.onComplete = {res in }
	}
	
	public init(name: String){
		self.action = {_ in }
		self.onComplete = {res in }
		self.name = name
	}
	
	public func plan(action: @escaping ()->Void){
		self.action = action
	}
	
	public func complete(result: T){
		self.onComplete(result)
	}
	
	@discardableResult public func run(onComplete: @escaping (T)->Void)->Task<T>{
		self.onComplete = onComplete
		self.action()
		return self
	}
	
}


// Asynchronous function execution chain
public class AsyncChain<T>{
	
	// Reference to first part of chain
	private var first: AsyncChain<T>?
	
	// Reference to next part of chain
	private var next: AsyncChain<T>?
	
	// Reference to executed function
	private let execFn: (T)->Void
	
	// Chain call parameter
	private let param: T
	
	public init(execFn: @escaping (T)->Void, param: T){
		self.execFn = execFn
		self.param = param
		self.first = self
	}
	
	init(execFn: @escaping (T)->Void, first: AsyncChain<T>){
		self.execFn = execFn
		self.first = first
		self.param = first.param
	}
	
	public func then(execFn: @escaping (T)->Void)->AsyncChain<T>{
		let nextPart = AsyncChain(execFn: execFn, first: self.first!)
		self.next = nextPart
		return nextPart
	}
	
	public func then(next: AsyncChain<T>)->AsyncChain<T>{
		self.next = next
		return next
	}
	
	public func run(){
		if self.first != nil {
			self.first!.runForward(with: self.first!.param)
		}
	}
	
	private func runForward(with:T){
		DispatchQueue.global(qos: DispatchQoS.QoSClass.default).async {
			self.execFn(with)
			if self.next != nil {
				self.next!.runForward(with: with)
			}
		}
	}
	
	
}


