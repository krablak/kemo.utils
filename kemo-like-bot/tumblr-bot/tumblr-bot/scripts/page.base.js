var jsPageApi = function(jsPageApi){	
	
	jsPageApi.isLoaded = function() {
		return "true";
	};
	
	jsPageApi.setValueTo = function(selector,value) {
		var resDesc = "";
		var element = document.querySelector(selector);
		if(element){
			element.value = value;
			resDesc = "Value '"+ value +"' was set to element " + element;
		}else{
			resDesc = "Value cannot be set. No element was found for selector " + selector;
		}
		return resDesc;
	};
	
	jsPageApi.submit = function(selector) {
		var resDesc = "";
		var element = document.querySelector(selector);
		if(element){
			element.submit();
			resDesc = "Submit was set to element " + element;
		}else{
			resDesc = "Cannot submit form. No element was found for selector " + selector;
		}
		return resDesc;
	};
	
	jsPageApi.exists = function(selector) {
		return document.querySelector(selector) ? "true" : "false";
	};
	
	jsPageApi.clickOn = function(selector) {
		var resDesc = "";
		var element = document.querySelector(selector);
		if(element){
			element.click();
			resDesc = "Clicked on " + element;
		}else{
			resDesc = "Cannot click. No element was found for selector " + selector;
		}
		return resDesc;
	};
	
	return jsPageApi;
}(jsPageApi || {});
