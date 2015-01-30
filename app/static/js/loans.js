$(document).ready(function() {
    //move_needle();
    tablesorter();
    color_table_rows_on_hover();
    color_table_rows_on_click();
    show_sliders();
    get_data_ajax();
    $('.loan-tr').click(function(){
        var tr_id = $(this).attr('id');
        reload_loan_detail(tr_id);
    });

});

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
            0: {sorter: "digit"}, 
            1: { sorter: "text" },
            2: { sorter: "digit" },
            3: { sorter: "currency" },
            4: { sorter: "digit" },
            5: { sorter: "digit" }
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

    /*
    This logic is too complex. Simplify it!
    */

    $("#node1").attr("fill", "#000");

    if ($('#' + loanId).next().attr('id') == 'tr-loan-detail') {   
        console.log($('#' + loanId).next().attr('id'));
        var loan_detail = $('#loan-detail').detach();
        $('#hidden').append(loan_detail);
        $('#tr-loan-detail').remove();
        $('#loan-detail').toggleClass("active", false);
        $('#' + loanId).children().css('background-color', 'white');
    } else {
        //check if loan-detail is already active. if so, hide it first
        if($("#loan-detail").hasClass("active")) {
            console.log($('#' + loanId).next().attr('id'));
            var loan_detail = $('#loan-detail').detach();
            $('#hidden').append(loan_detail);
            $('#tr-loan-detail').remove();
            $('#loan-detail').toggleClass("active", false);
            $('#' + loanId).children().css('background-color', 'white');
        }
        $('#' + loanId).after('<tr id="tr-loan-detail"><td colspan="7" id="td-loan-detail"></td></tr>');
        $('#td-loan-detail').append($('#loan-detail'));
        $('#loan-detail').toggleClass("active", true);

        
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
    $('.loan-tr')
        .mouseenter(function() {
             $(this).children().css('background-color', '#8dbdd8');
             console.log($(this).attr("id"));
             //color plot data point on hover
             $("#node_" + $(this).attr("id")).attr("r", 15);
    })
      .mouseleave(function() {
             $(this).children().css('background-color', 'white');
             $("#node_" + $(this).attr("id")).attr("r", 6);
    });

};

function color_table_rows_on_click() {
    $('.loan-tr').click(function() {
        $(this).children().css('background-color', '#8dbdd8');
    });
}

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
                //update the graph
                var blue_x_values = [];
                for(i in json['loans']) {
                    blue_x_values.push(json['loans'][i]['index']);
                }
                get_data_ajax(blue_x_values);
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
                //update the graph
                var blue_x_values = [];
                for(i in json['loans']) {
                    blue_x_values.push(json['loans'][i]['index']);
                }
                get_data_ajax(blue_x_values);
                
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
        var pred_roi = loans['loans'][i]['pred_roi'];
        var pred_default = loans['loans'][i]['pred_default'];
        var pred_default_time = loans['loans'][i]['pred_default_time'];
        var pred_default_error = loans['loans'][i]['pred_default_error'];
        var pred_default_time_error = loans['loans'][i]['pred_default_time_error'];
        var html_to_append = '<tr class="loan-tr tr-active" id="' + id + '"> \
                                <td>' + index + '</td> \
                                <td>' + grade + '</td> \
                                <td>' + intRate + '%</td> \
                                <td>$' + loanAmnt + '</td> \
                                <td>' + pred_roi + '%</td> \
                                <td>' + pred_default + '&#177; ' + pred_default_error + '</td> \
                                <td>' + pred_default_time + '&#177; ' + pred_default_time_error + '</td> \
                              </tr>'
        $("#topTable").append(html_to_append)
    }
    color_table_rows_on_hover();
    
    //reset tablesorter
    $(".tablesorter").trigger("update"); 
};

function draw_d3_chart(container, data) {
    //plots data in blue, data_grey in grey
    //data_grey has no hover or tooltip
    var w = 600;
    var h = 300;
    var padding = 60;

    //delete the current graph if it exists
    $("#" + container + " svg").remove();

    data = data.filter(function(el) {
        return !isNaN(parseFloat(el[1]));
    });
 
    var xScale = d3.scale.linear()
                         .domain([d3.min(data, function(d) {return parseFloat(d[1]);}),
                                  d3.max(data, function(d) {return parseFloat(d[1]);})])
                         .range([padding, w - padding]);
    var yScale = d3.scale.linear()
                         .domain([d3.min(data, function(d) {return parseFloat(d[2]);}),
                                  d3.max(data, function(d) {return parseFloat(d[2]);})])
                         .range([h - padding, padding]);
    var rScale = d3.scale.sqrt()
                         .domain([0, d3.max(data, function(d) {return d[2];})])
                         .range([2, 8]);

    var svg = d3.select("#" + container)
                .append("svg")
                .attr("width", w)
                .attr("height", h)
                .attr("padding", padding);
    
    svg.selectAll("circle")
       .data(data)
       .remove();
    

    var xAxis = d3.svg.axis()
                      .scale(xScale)
                      .orient("bottom")
                      .ticks(5);
    var yAxis = d3.svg.axis()
                      .scale(yScale)
                      .orient("left")
                      .ticks(5)
                      .tickSize(-(w-2*padding), 0, 0);
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

    //axis labels
    svg.append("text")
      .attr("x", (w-2*padding)/2-50)
      .attr("y", h-5)
      .attr("class", "axis_label")
      .text("Default Probability (%)");
    svg.append("text")
      .attr("y", 15)
      .attr("x", -(h-2*padding)/2)
      .attr("class", "rotate")
      .classed("axis_label", true)
      .attr("text-anchor", "end")
      .text("Estimated ROI (%)");
    //title
    svg.append("text")
      .attr("x", (w-2*padding)/2-75)
      .attr("y", 20)
      .attr("class", "title")
      .text("ROI vs Default Probability");

    //add blue data points
    var circles = svg.selectAll("circle")
       .data(data)
       .enter()
       .append("circle")
       .attr({
            cx : function(d) {return xScale(d[1]);},
            cy : function(d) {return yScale(d[2]);},
            r : 6,
            "class" : "blue_circle",
            "fill" : function(d) {return get_circle_color(d[2], d[3]);},
            "id" : function(d) {return "node_" + String(d[0]);}            
       })
       .on("click", function(d) {
            console.log(d);
        })
       .on("mouseover", function(d) {
            if(d[3] == 1) {

                d3.select("#tooltip-" + container)
                  .style("left", d3.event.pageX-20 + "px")
                  .style("top", d3.event.pageY+30 + "px")
                  .select("#tooltip-id")
                  .text(d[0]);
                d3.select("#tooltip-" + container)
                  .select("#tooltip-roi")
                  .text(d[2]);
                d3.select("#tooltip-" + container).classed("hidden", false);
                d3.select(this)
                  .attr("r", 14)
                  .attr("class", "circle-blue");
            }
       })
       .on("mouseout", function() {
                d3.select("#tooltip-" + container).classed("hidden", true);
                d3.select(this)
                  .attr("r", 6);

        });
       
    function get_circle_color(roi, active) {
        if(active == 0) {
            return "#d3d3d3";
        } 
        else {
            //color points based on ROI
            if(roi >= 0.5) {
                return "green";
            }
            else if(roi < 0.5 && roi > -2.0) {
                return "orange";
            }
            else {
                return "red";    
            }
            
        }
    }
};

function get_data_ajax(blue_x_values) {
    $.getJSON("./roi", function(json) {
        var data_roi = [];
        for (i in json['default_prob']) {
            var default_prob = json['default_prob'][i] * 100;
            var loan_id = parseFloat(json['loan_id'][i]);
            var roi = json['roi'][i];
            //var loan_id = parseInt(i)+1;  //keep graph aligned with table
            var active = 0;
            if(typeof(blue_x_values) == "undefined") {
                active = 1;
            }
            else if($.inArray(parseFloat(i)+1, blue_x_values) != -1) {
                active = 1;
            }
            data_roi.push([loan_id, default_prob, roi, active]);
        }
        draw_d3_chart("d3-chart-left", data_roi);   
        });
    };



