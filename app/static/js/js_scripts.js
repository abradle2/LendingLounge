$(document).ready(function() {
    tablesorter();
    default_prob_chart();
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


function default_prob_chart() {
      // Create a Bar Chart with Morris
      var chart = Morris.Line({
        // ID of the element in which to draw the chart.
        element: 'default-prob-chart',
        data: [0, 0], // Set initial data (ideally you would provide an array of default data)
        xkey: 'loan_id', // Set the key for X-axis
        ykeys: ['default_prob'], // Set the key for Y-axis
        labels: ['Orders'] // Set the label when bar is rolled over
      });

      // Fire off an AJAX request to load the data
      $.ajax({
          console.log('firing ajax');
          type: "GET",
          dataType: 'json',
          url: "/default_prob", // This is the URL to the API
          data: {} // Passing a parameter to the API to specify number of days
        })
        .done(function( data ) {
          // When the response to the AJAX request comes back render the chart with new data
          alert(data);
          chart.setData(data);
        })
        .fail(function() {
          // If there is no communication between the server, show an error
          alert( "error occured" );
        });
    
};

