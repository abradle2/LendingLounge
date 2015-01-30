$(document).ready(function () {
    //loan status plot
    $('#loan-status-plot').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Loan Status Breakdown'
        },
        xAxis: {
            categories: ['Paid On Time', 'Prepaid', 'Default']
        },
        yAxis: {
            title: {
                text: '% of Loans',
                style: {
                    fontSize: '20px'
                }
            }
        },

        legend: {
            enabled: false
        },
        series: [{
            //name: 'Days Since Loan Origination',
            data: [27, 57, 16]
        }]
    });

    //default histogram
    $('#default-hist').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Time to Default'
        },
        xAxis: {
            categories: ['-20',
                         '76',
                         '174',
                         '272',
                         '370',
                         '467',
                         '565',
                         '663',
                         '761',
                         '858',
                         '956',
                         '1054',
                         '1152',
                         '1249',
                         '1347',
                         '1445',
                         '1542',
                         '1640',
                         '1738',
                         '1836'],
            title: {
                text: 'Days Since Loan Origination',
                style: {
                    fontSize: '20px'
                }
            }
        },
        yAxis: {
            title: {
                text: 'Number of Loans',
                style: {
                    fontSize: '20px'
                }
            }
        },

        legend: {
            enabled: false
        },
        series: [{
            //name: 'Days Since Loan Origination',
            data: [  3.00000000e+02,   8.19000000e+02,   1.00600000e+03,
                     1.52500000e+03,   1.00000000e+03,   9.55000000e+02,
                     8.18000000e+02,   6.88000000e+02,   4.05000000e+02,
                     2.45000000e+02,   1.47000000e+02,   5.90000000e+01,
                     7.00000000e+00,   6.00000000e+00,   5.00000000e+00,
                     2.00000000e+00,   3.00000000e+00,   0.00000000e+00,
                     0.00000000e+00,   1.00000000e+00]
        }]
    });

    //prepaid histogram
    $('#prepaid-hist').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Time to Prepay'
        },
        xAxis: {
            categories: ['25',
                         '77',
                         '128',
                         '179',
                         '231',
                         '282',
                         '333',
                         '385',
                         '436',
                         '488',
                         '539',
                         '590',
                         '642',
                         '693',
                         '744',
                         '796',
                         '847',
                         '898',
                         '950',
                         '1001'],
            title: {
                text: 'Days Since Loan Origination',
                style: {
                    fontSize: '20px'
                }
            }
        },
        yAxis: {
            title: {
                text: 'Number of Loans',
                style: {
                    fontSize: '20px'
                }
            }
        },

        legend: {
            enabled: false
        },
        series: [{
            //name: 'Days Since Loan Origination',
            data: [  5.00000000e+00,   4.28600000e+03,   3.85000000e+03,
                     1.98700000e+03,   4.51400000e+03,   5.36000000e+03,
                     2.45200000e+03,   4.65100000e+03,   4.19600000e+03,
                     3.63800000e+03,   1.84800000e+03,   3.14000000e+03,
                     2.82700000e+03,   1.33400000e+03,   2.33300000e+03,
                     1.97200000e+03,   9.51000000e+02,   1.55500000e+03,
                     1.49000000e+03,   6.38000000e+02]
        }]
    });

    //Random Forest Convergence
    $('#random-forest-plot').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'Convergence of Random Forest'
        },
        xAxis: {
            categories: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 300, 500, 1000],
            title: {
                text: 'Number of Trees in Forest',
                style: {
                    fontSize: '20px'
                }
            }
        },
        yAxis: {
            title: {
                text: 'Coefficient of Determination',
                style: {
                    fontSize: '20px'
                }
            }
        },

        legend: {
            enabled: true
        },
        series: [{
            name: 'Training Set',
            data: [0.93, 0.94, 0.94, 0.94, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]
        },
        {
            name: 'Test Set',
            data: [0.53, 0.56, 0.59, 0.58, 0.58, 0.59, 0.58, 0.58, 0.59, 0.59, 0.59, 0.59, 0.59]
        }]
    });

    //case study plot
    $('#case-study-plot').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'ROI for Various Investment Strategies'
        },
        xAxis: {
            categories: ['Random', 'Lowest DTI', 'Highest Int Rate', 'Loan Quickr Pickr']
        },
        yAxis: {
            title: {
                text: 'Actual ROI (%)',
                style: {
                    fontSize: '20px'
                }
            }
        },

        legend: {
            enabled: false
        },
        series: [{
            //name: 'Days Since Loan Origination',
            data: [0.0, 4.4, 2.8, 9.3]
        }]
    });
});