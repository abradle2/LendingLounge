var loans_on_page = [];
var grade_shown;
var num_loans_shown = 0;
$(document).ready(function() {
	
	$("#A-btn").click(function() {
		//remove active loan thumbnails
		$(".loan-thumbnail-active").find(".x").trigger("click");
		loans_on_page = [];
		grade_shown = 'A';
		load_loan();

	});
	$("#B-btn").click(function() {
		$(".loan-thumbnail-active").find(".x").trigger("click");
		loans_on_page = [];
		grade_shown = 'B';
		load_loan();
	});
	$("#C-btn").click(function() {
		$(".loan-thumbnail-active").find(".x").trigger("click");
		loans_on_page = [];
		grade_shown = 'C';
		load_loan();
	});

	$("#more-loans").click(function() {
		load_loan();
	});
	$("#more-loans").mouseover(function() {
		$(this).css("cursor", "pointer");
	});
	$(".x").click(function() {
		$(this).parent().remove();
		num_loans_shown --;
		if(num_loans_shown == 0) {
			$("#more-loans").toggleClass("hidden", true);
			$("#index-loan-detail").toggleClass("hidden", true);
		}

	});
	$(".loan-thumbnail").click(function() {
		reload_loan_detail($(this).attr("id"));
		$(".loan-thumbnail").toggleClass("loan-thumbnail-highlighted", false);
		$(this).toggleClass("loan-thumbnail-highlighted", true);
		$("#index-loan-detail").toggleClass("hidden", false);
	});
	$(".loan-thumbnail").mouseover(function() {
		$(this).css("cursor", "pointer");
	});

});

function reload_loan_detail(loan_id) {
        
    $.getJSON("./loan", {'loanId':loan_id}, function(json) {        
        //Update all the loan detail divs
        $('#index-loan-id').text(json['loan']['id'])
        $('#index-loan-grade').text(json['loan']['grade'])
        $('#index-loan-roi').text(json['loan']['pred_roi'])
        $('#index-loan-borrowerId').text(json['loan']['memberId'])
        $('#index-loan-acceptD').text(json['loan']['acceptD'])
        $('#index-loan-installment').text(json['loan']['installment'])
        $('#index-loan-reviewStatus').text(json['loan']['reviewStatus'])
        $('#index-loan-id').text(json['loan']['id'])
        $('#index-loan-dti').text(json['loan']['dti'])
        $('#index-loan-annualInc').text(json['loan']['annualInc'])
        $('#index-loan-homeOwnership').text(json['loan']['homeOwnership'])
        $('#index-loan-empLength').text(json['loan']['empLength']/10)
        $('#index-loan-occupation').text(json['loan']['occupation'])
        $('#index-loan-location').text(json['loan']['addrZip'] + ', ' + json['loan']['addrState'])
        $('#index-loan-ficoRange').text(json['loan']['ficoRangeLow'] + ' - ' + json['loan']['ficoRangeHigh'])
        $('#index-loan-earliestCrLine').text(json['loan']['earliestCrLine'])
        $('#index-loan-openAccts').text(json['loan']['openAccts'])
        $('#index-loan-totalAcc').text(json['loan']['totalAcc'])
        $('#index-loan-revolBal').text(json['loan']['revolBal'])
        $('#index-loan-revolUtil').text(json['loan']['revolUtil'])
        $('#index-loan-inqLast6Mths').text(json['loan']['inqLast6Mths'])
        $('#index-loan-accNowDelinq').text(json['loan']['accNowDelinq'])
        $('#index-loan-delinqAmnt').text(json['loan']['delinqAmnt'])
        $('#index-loan-delinq2Yrs').text(json['loan']['delinq2Yrs'])
        $('#index-loan-mthsSinceLastDelinq').text(json['loan']['mthsSinceLastDelinq'])
        $('#index-loan-pubRec').text(json['loan']['pubRec'])
        $('#index-loan-mthsSinceLastRecord').text(json['loan']['mthsSinceLastRecord'])
        $('#index-loan-mthsSinceLastDerog').text(json['loan']['mthsSinceLastDerog'])
        $('#index-loan-collections12MthsExMed').text(json['loan']['collections12MthsExMed'])
        $('#index-loan-description').text(json['loan']['description'])
        $('#index-loan-default-prob').text(json['loan']['pred_default'])
        $('#index-loan-default-prob-error').text(json['loan']['pred_default_error'])
        $('#index-loan-prepaid-prob').text(json['loan']['pred_prepaid'])
        $('#index-loan-prepaid-prob-error').text(json['loan']['pred_prepaid_error'])
    });
};

function load_loan() {
	var prev_loan_id = loans_on_page[loans_on_page.length-1];
	$.getJSON("./loan_recommendation", {'grade':grade_shown, 'prev_loan_id':prev_loan_id}, function(json) {
		var loan_id = json['loan']['id'];
		var state = json['loan']['addrState']
		loans_on_page.push(loan_id)
		var loan_clone = $("#loan-thumbnail-div").clone(true);
		loan_clone.attr("id", loan_id);
		loan_clone.toggleClass("loan-thumbnail-active", true);
		loan_clone.appendTo($("#index-main-left-content"));

		loan_clone.find("#loan-thumbnail-grade").text(json['loan']['grade']);
		loan_clone.find("#loan-thumbnail-id").text(loan_id);
		loan_clone.find("#loan-thumbnail-roi").text(json['loan']['pred_roi']);
		loan_clone.find("#loan-thumbnail-amount").text(json['loan']['loanAmnt']);
		loan_clone.find("#loan-thumbnail-int-rate").text(json['loan']['intRate']);
		loan_clone.find("#loan-thumbnail-installment").text(json['loan']['installment']);
		loan_clone.find("#loan-thumbnail-term").text(json['loan']['term']);
		//reload_loan_detail(loan_id);
		num_loans_shown ++;
		//give map an id equal
		var map_div_id = "map-" + loan_id
		loan_clone.find("#map").attr("id", map_div_id);
		
		show_map(map_div_id, state);
		$("#more-loans").toggleClass("hidden", false);
	});
};

function show_map(el, state) {
	console.log(el);
	var winOH = '#0f00f0';
	//this is super hacky but the only thing we could figure out
	var map_code = "var map = new Datamap({ \
		element: document.getElementById(el), \
		scope: 'usa', \
		fills: { \
			defaultFill: '#D6D6D6', \
			win: '#FF0000' \
		}, \
		data: {'" + state +"': { fillKey: 'win'} } \
	});"
	eval(map_code);
	//hack to hide annoying tooltip
	$(".datamaps-hoverover").css("opacity", "0");

};

