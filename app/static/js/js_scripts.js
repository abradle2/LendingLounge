$(document).ready(function() {
    tablesorter();
    draw_default_prob_chart([[1,2], [3,3]]);
    draw_roi_chart([0,0], [1,1]);
    $('.loan-tr').click(function(){
        var tr_id = $(this).attr('id');
        reload_loan_detail(tr_id);
    });
});

function draw_default_prob_chart(data) {

    var options = {
        chart: {
                renderTo: 'default-prob-chart',
                type: 'scatter',
                height: 200
            },
        title: {
            text: 'Predicted Default Probability',
            x: -20 //center
        },
        xAxis: {
            categories: []
        },
        yAxis: {
            title: {
                text: 'Probability of Default (%)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        xAxis: {
            title: {
                text: 'Loan Number'
            },
            labels: {
                enabled: false
            }
        },
        legend: {
            display: false
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>Loan {point.x}<br>{point.y}%</b><br>',
                    pointFormat: ''
                }
            }
        },
        series: [{
            data: []
        }]
    }
    $.getJSON("./default_prob", function(json) {        
        options.series[0].data = json['default_prob'];
        options.xAxis.categories = json['index'];
        chart = new Highcharts.Chart(options);
    });
};

function draw_roi_chart(data) {

    var options = {
        chart: {
                renderTo: 'roi-chart',
                type: 'scatter',
                height: 200
            },
        title: {
            text: 'Predicted Default Probability',
            x: -20 //center
        },
        xAxis: {
            categories: []
        },
        yAxis: {
            title: {
                text: 'Probability of Default (%)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        xAxis: {
            title: {
                text: 'Loan Number'
            },
            labels: {
                enabled: false
            }
        },
        legend: {
            display: false
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>Loan {point.x}<br>{point.y}%</b><br>',
                    pointFormat: ''
                }
            }
        },
        series: [{
            data: []
        }]
    }
    $.getJSON("./default_prob", function(json) {        
        options.series[0].data = json['default_prob'];
        options.xAxis.categories = json['index'];
        chart = new Highcharts.Chart(options);
    });
};


function tablesorter() {
    $('.tablesorter').tablesorter({
        // *** Appearance ***
        // fix the column widths
        widthFixed : true,
        // include zebra and any other widgets, options:
        // 'uitheme', 'filter', 'stickyHeaders' & 'resizable'
        // the 'columns' widget will require custom css for the
        // primary, secondary and tertiary columns
      
        // other options: "ddmmyyyy" & "yyyymmdd"
        dateFormat : "mmddyyyy",

        // *** Functionality ***
        // starting sort direction "asc" or "desc"
        sortInitialOrder : "asc",
        // These are detected by default,
        // but you can change or disable them
        headers : {
            // set "sorter : false" (no quotes) to disable the column
            0: { sorter: "text" },
            1: { sorter: "digit" },
            2: { sorter: "text" },
            3: { sorter: "url" }
        },
        // extract text from the table - this is how is
        // it done by default
        textExtraction : {
            0: function(node) { return $(node).text(); },
            1: function(node) { return $(node).text(); }
        },
        // forces the user to have this/these column(s) sorted first
        sortForce : null,
        // initial sort order of the columns
        // [[columnIndex, sortDirection], ... ]
        sortList : [[3,0]],
        // default sort that is added to the end of the users sort
        // selection.
        sortAppend : null,
        // Use built-in javascript sort - may be faster, but does not
        // sort alphanumerically
        sortLocaleCompare : false,
        // Setting this option to true will allow you to click on the
        // table header a third time to reset the sort direction.
        sortReset: false,
        // Setting this option to true will start the sort with the
        // sortInitialOrder when clicking on a previously unsorted column.
        sortRestart: false,
        // The key used to select more than one column for multi-column
        // sorting.
        sortMultiSortKey : "shiftKey",

        // *** Customize header ***
        onRenderHeader  : function() {
            // the span wrapper is added by default
            $(this).find('span').addClass('headerSpan');
        },
        // jQuery selectors used to find the header cells.
        selectorHeaders : 'thead th',

        // *** css classes to use ***
        cssAsc        : "headerSortUp",
        cssChildRow   : "expand-child",
        cssDesc       : "headerSortDown",
        cssHeader     : "header",
        tableClass    : 'tablesorter',

        // *** widget css class settings ***
        // column classes applied, and defined in the skin
        widgetColumns : { css: ["primary", "secondary", "tertiary"] },
        // find these jQuery UI class names by hovering over the
        // Framework icons on this page:
        // http://jqueryui.com/themeroller/
        widgetUitheme : { css: [
            "ui-icon-arrowthick-2-n-s", // Unsorted icon
            "ui-icon-arrowthick-1-s",   // Sort up (down arrow)
            "ui-icon-arrowthick-1-n"    // Sort down (up arrow)
            ]
        },
        // pick rows colors to match ui theme
        widgetZebra: { css: ["ui-widget-content", "ui-state-default"] },

        // *** prevent text selection in header ***
        cancelSelection : true,

        // *** send messages to console ***
        debug : false
    });
};

function reload_loan_detail(loanId) {
    $.getJSON("./loan", {'loanId':loanId}, function(json) {        
        //Update all the loan detail divs
        $('#loan-acceptD').text(json['loan']['acceptD'])
        $('#loan-installment').text(json['loan']['installment'])
        $('#loan-reviewStatus').text(json['loan']['reviewStatus'])
        $('#loan-id').text(json['loan']['id'])
        $('#loan-dti').text(json['loan']['dti'])
        $('#loan-annualInc').text(json['loan']['annualInc'])
        $('#loan-homeOwnership').text(json['loan']['homeOwnership'])
        $('#loan-empLength').text(json['loan']['empLength'])
        $('#loan-occupation').text(json['loan']['occupation'])
        $('#loan-location').text(json['loan']['addrZip'] + ', ' + json['loan']['addrState'])
        $('#loan-ficoRange').text(json['loan']['ficoRangeLow'] + ' - ' + json['loan']['ficoRangeHigh'])
        $('#loan-earliestCrLine').text(json['loan']['earliestCrLine'])
        $('#loan-openAccts').text(json['loan']['openAccts'])
        $('#loan-totalAcc').text(json['loan']['totalAcc'])
        $('#loan-revolBal').text(json['loan']['revolBal'])
        $('#loan-revolUtil').text(json['loan']['revolUtil'])
        $('#loan-inqLast6Mths').text(json['loan']['inqLast6Mths'])
        $('#loan-accNowDelinq').text(json['loan']['accNowDelinq'])
        $('#loan-delinqAmnt').text(json['loan']['delinqAmnt'])
        $('#loan-delinq2Yrs').text(json['loan']['delinq2Yrs'])
        $('#loan-mthsSinceLastDelinq').text(json['loan']['mthsSinceLastDelinq'])
        $('#loan-pubRec').text(json['loan']['pubRec'])
        $('#loan-mthsSinceLastRecord').text(json['loan']['mthsSinceLastRecord'])
        $('#loan-mthsSinceLastDerog').text(json['loan']['mthsSinceLastDerog'])
        $('#loan-collections12MthsExMed').text(json['loan']['collections12MthsExMed'])
        $('#loan-description').text(json['loan']['description'])
    });
};

