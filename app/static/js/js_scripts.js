$(document).ready(function() {
    move_needle();
    tablesorter();
    draw_default_prob_chart([[1,2], [3,3]]);
    draw_roi_chart([0,0], [1,1]);
    color_table_rows_on_hover();
    show_sliders();
    draw_d3_chart([[0,0], [1,1]]);
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
            enabled: false
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
            text: 'Predicted Days Until Default',
            x: -20 //center
        },
        xAxis: {
            categories: []
        },
        yAxis: {
            title: {
                text: 'Days Until Predicted Default'
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
            enabled: false
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
                    headerFormat: '<b>Loan {point.x}<br>{point.y} days</b><br>',
                    pointFormat: ''
                }
            }
        },
        series: [{
            data: []
        }]
    }
    $.getJSON("./default_prob", function(json) {
        options.series[0].data = json['pred_default_time'];
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
    //show loan details if clicking on a row, hide it if click again
    //console.log($('#' + loanId).next().attr('id'));
    if ($('#' + loanId).next().attr('id') == 'tr-loan-detail') {   
        console.log($('#' + loanId).next().attr('id'));
        var loan_detail = $('#loan-detail').detach();
        $('#hidden').append(loan_detail);
        $('#tr-loan-detail').remove();
        $('#' + loanId).children().css('background-color', 'white');
    } else {
        $('#' + loanId).after('<tr id="tr-loan-detail"><td colspan="6" id="td-loan-detail"></td></tr>');
        $('#td-loan-detail').append($('#loan-detail'));
        $('li').css('list-style', 'none');
        
    }
    $.getJSON("./loan", {'loanId':loanId}, function(json) {        
        //Update all the loan detail divs
        $('#loan-borrowerId').text(json['loan']['memberId'])
        $('#loan-acceptD').text(json['loan']['acceptD'])
        $('#loan-installment').text(json['loan']['installment'])
        $('#loan-reviewStatus').text(json['loan']['reviewStatus'])
        $('#loan-id').text(json['loan']['id'])
        $('#loan-dti').text(json['loan']['dti'])
        $('#loan-annualInc').text(json['loan']['annualInc'])
        $('#loan-homeOwnership').text(json['loan']['homeOwnership'])
        $('#loan-empLength').text(json['loan']['empLength']/10)
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

function move_needle() {
    var pos = $('#needle').position();
    var delta_x = 10;
    $('#needle').css("position", "relative")
    if(pos.left < 1000) {
        var x = String(pos.left + delta_x) + "px";
        $('#needle').css("left", x);
    }
    else {
        $('#needle').css("left", 0);
    }
    setTimeout('move_needle()',100);
};

function color_table_rows_on_hover() {
    $('.loan-tr').click(function(){
        var tr_id = $(this).attr('id');
        reload_loan_detail(tr_id);
    });
    $('.loan-tr')
        .mouseenter(function() {
             $(this).children().css('background-color', '#8dbdd8');
    })
      .mouseleave(function() {
             $(this).children().css('background-color', 'white');
    });
};

function show_sliders() {
    var int_rate_min = 0
    var int_rate_max = 30
    var est_default_min = 0
    var est_default_max = 100
    $( "#int-rate-slider" ).slider({
      range: true,
      min: int_rate_min,
      max: int_rate_max,
      values: [ int_rate_min, int_rate_max ],
      slide: function( event, ui ) {
        $( "#int-rate-value" ).val( ui.values[ 0 ] + "% - " + ui.values[ 1 ] + "%" );
        int_rate_min = ui.values[0];
        int_rate_max = ui.values[1];
      },
      change: function(event, ui) {
        $.getJSON("./loans-filtered", 
            {   int_rate_min: int_rate_min, 
                int_rate_max: int_rate_max,
                est_default_min: est_default_min,
                est_default_max: est_default_max },
            function(json) {
                update_table(json);
                
        });
      }
    });

    //update the slider label on page load
    $( "#int-rate-value" ).val( $( "#int-rate-slider" ).slider( "values", 0 ) +
        "% - " + $( "#int-rate-slider" ).slider( "values", 1 ) + "%" );

    $( "#est-default-slider" ).slider({
      range: true,
      min: est_default_min,
      max: est_default_max,
      values: [ est_default_min, est_default_max ],
      slide: function( event, ui ) {
        $( "#est-default-value" ).val( ui.values[ 0 ] + "% - " + ui.values[ 1 ] + "%" );
        est_default_min = ui.values[0];
        est_default_max = ui.values[1];
      },
      change: function(event, ui) {
        $.getJSON("./loans-filtered", 
            {   int_rate_min: int_rate_min, 
                int_rate_max: int_rate_max,
                est_default_min: est_default_min,
                est_default_max: est_default_max },
            function(json) {
                update_table(json);
                
        });
      }
    });
    //update the slider label on page load
    $( "#est-default-value" ).val( $( "#est-default-slider" ).slider( "values", 0 ) +
        "% - " + $( "#est-default-slider" ).slider( "values", 1 ) + "%" );
}

function update_table(loans) {
    //Remove the currently displayed loans and update table
    $(".loan-tr").remove();
    for (i in loans['loans']) {
        var id = loans['loans'][i]['id'];
        var index = loans['loans'][i]['index'];
        var grade = loans['loans'][i]['grade'];
        var intRate = loans['loans'][i]['intRate'];
        var loanAmnt = loans['loans'][i]['loanAmnt'];
        var pred_default = loans['loans'][i]['pred_default'];
        var pred_default_time = loans['loans'][i]['pred_default_time'];
        var html_to_append = '<tr class="loan-tr tr-active" id="' + id + '"> \
                                <td>' + index + '</td> \
                                <td>' + grade + '</td> \
                                <td>' + intRate + '</td> \
                                <td>' + loanAmnt + '</td> \
                                <td>' + pred_default + '</td> \
                                <td>' + pred_default_time + '</td> \
                              </tr>'
        $("#topTable").append(html_to_append)
    }
    color_table_rows_on_hover();
};

function draw_d3_chart(data) {
    var w = 500;
    var h = 200;
    var padding = 40;
    get_data_ajax();
    dataset = data;
    // dataset = [
    //                 [5, 20], [480, 90], [250, 50], [100, 33], [330, 95],
    //                 [410, 12], [475, 44], [25, 67], [85, 21], [220, 88]
    //               ];

    var xScale = d3.scale.linear()
                         .domain([0, d3.max(dataset, function(d) {return d[0];})])
                         .range([padding, w - padding]);
    var yScale = d3.scale.linear()
                         .domain([0, d3.max(dataset, function(d) {return d[1];})])
                         .range([h - padding, padding]);
    var rScale = d3.scale.sqrt()
                         .domain([0, d3.max(dataset, function(d) {return d[1];})])
                         .range([2, 8]);

    var svg = d3.select("#d3-chart")
                .append("svg")
                .attr("width", w)
                .attr("height", h)
                .attr("padding", padding);
    svg.selectAll("circle")
       .data(dataset)
       .enter()
       .append("circle")
       .attr({
            cx : function(d) {return xScale(d[0]);},
            cy : function(d) {return yScale(d[1]);},
            r : function(d) {return rScale(d[1]);} 
       })
       .on("click", function(d) {
            console.log(d);
        })
       .on("mouseover", function(d) {
            var xPos = parseFloat(d3.select(this).attr("cx") + 30);
            var yPos = parseFloat(d3.select(this).attr("cy")) + 30;
            d3.select("#tooltip")
              .style("left", xPos + "px")
              .style("top", yPos, + "px")
              .select("#value")
              .text(d);
            d3.select("#tooltip").classed("hidden", false);
       })
       .on("mouseout", function() {
            d3.select("#tooltip").classed("hidden", true);
       });

    //var formatAsPercentage = d3.format(".1%");
    var xAxis = d3.svg.axis()
                      .scale(xScale)
                      .orient("bottom")
                      .ticks(5);
                      //.tickFormat(formatAsPercentage);
    var yAxis = d3.svg.axis()
                      .scale(yScale)
                      .orient("left")
                      .ticks(5);
    svg.append("g")
        .attr("id", "x_axis")
        .attr("class", "axis")
        .attr("transform", "translate(0," + (h - padding) + ")" )
        .call(xAxis);

    svg.append("g")
        .attr("id", "y_axis")
        .attr("class", "axis")
        .attr("transform", "translate(" + padding + ",0)" )
        .call(yAxis);


    function get_data_ajax() {
        $.getJSON("./default_prob", function(json) {
            var data = [];
            for (i in json['default_prob']) {
                var default_prob = json['default_prob'][i];
                var loan_id = i;
                data.push([loan_id, default_prob]);
            }
            redraw_d3(data);
        });
    };

    function redraw_d3(data) {
        
        xScale.domain([0, d3.max(data, function(d) {return d[0];})]);
        //yScale.domain([0, d3.max(data, function(d) {return d[1];})]);
        yScale.domain([0, 1]);
        rScale.domain([0, d3.max(data, function(d) {return d[1];})])
        xAxis.scale(xScale);
        yAxis.scale(yScale);

        svg.select("#x_axis")
           .call(xAxis);
        svg.select("#y_axis")
            .call(yAxis);

        //remove all data points
        svg.selectAll("circle")
           .data(dataset)
           .remove();

        //add new data points
        svg.selectAll("circle")
           .data(data)
           .enter()
           .append("circle")
           .attr({
                cx : function(d) {return xScale(d[0]);},
                cy : function(d) {return yScale(d[1]);},
                r : function(d) {return rScale(d[1]);} 
            })
           .on("click", function(d) {
            console.log(d);
        })
       .on("mouseover", function(d) {
            var xPos = parseFloat(d3.select(this).attr("cx"));
            var yPos = parseFloat(d3.select(this).attr("cy"));
            d3.select("#tooltip")
              .style("left", xPos + "px")
              .style("top", yPos, + "px")
              .select("#value")
              .text(d);
            d3.select("#tooltip").classed("hidden", false);
       })
       .on("mouseout", function() {
            d3.select("#tooltip").classed("hidden", true);
       });

       //axis labels
       svg.append("text")
          .attr("x", w/2)
          .attr("y", h)
          .attr("class", "axis_label")
          .text("Loan ID");
        svg.append("text")
          .attr("y", 10)
          .attr("x", -25)
          .attr("class", "rotate")
          .attr("text-anchor", "end")
          .text("Est. Default Probability");
    }
};



