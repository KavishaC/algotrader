
const RED_BORDER = 'rgba(255, 75, 66, 1)'
const RED_BACKGROUND = 'rgba(255, 75, 66, 0.15)'

const GREEN_BORDER = 'rgba(100, 220, 150, 1)'
const GREEN_BACKGROUND = 'rgba(100, 220, 150, 0.15)'

const TOOLTIP_COLOR = 'rgba(13, 110, 253, 1)'

document.addEventListener('DOMContentLoaded', function () {
    
    // Sample data
    console.log("{{ user_timezone }}")
    var price_data = {{ portfolio.price_data|safe }};
    
    // Create portfolio value chart
    var ctx = document.getElementById('assetValue').getContext('2d');
    ctx.canvas.width = '898px';
    ctx.canvas.height = '150px';
    //console.log(dateLabels)
    
    portfolioChangeStatus = "{{ portfolio.change_status }}";
    if (portfolioChangeStatus === "NEGATIVE") {
        borderColor = RED_BORDER;
        backgroundColor = RED_BACKGROUND;
    } else {
        borderColor = GREEN_BORDER;
        backgroundColor = GREEN_BACKGROUND;
    }
    
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: price_data["date"],
            datasets: [{
                data: price_data["value"],
                fill: true,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 3,
                pointRadius: 10,
                pointBorderColor: 'rgba(100, 220, 150, 0)',
                pointBackgroundColor: 'rgba(100, 220, 150, 0)',
                pointHoverRadius: 10,
                pointHoverBackgroundColor: borderColor,
                pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
                pointHoverBorderWidth: 3,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'DD'
                    },
                    ticks: {
                        maxTicksLimit: 4, // Set the maximum number of x-axis labels
                        maxRotation: 0,   // Set the maximum label rotation angle
                        minRotation: 0,
                        align: 'start',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },  
                    },
                    grid: {
                        tickColor: 'rgba(255, 255, 255, 1)'
                    }
                },
                y: {
                    beginAtZero: false,
                    position: 'right',
                    ticks: {
                        // You can add additional y-axis tick options here if needed
                        maxTicksLimit: 4, // Set the maximum number of x-axis labels
                        includeBounds: true,
                        crossAlign: 'far',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },  
                    },
                    grid: {
                        tickColor: 'rgba(255, 255, 255, 1)'
                    }
                }
            },
            animation: false,
            tooltips: {
                intersect: false,
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    mode: 'index',
                    displayColors: false,
                    backgroundColor: 'rgba(255, 255, 255, 1)',
                    titleColor: 'rgba(0, 0, 0, 1)',
                    bodyColor: 'rgba(0, 0, 0, 1)',
                    padding: 12,
                    cornerRadius: 12,
                    caretPadding: 12,
                    caretSize: 8,
                    bodyAlign: 'right'
                }
            },
        }
    });
    
    var ctx = document.getElementById('allocation_chart').getContext('2d');
    ctx.canvas.width = '898px';
    ctx.canvas.height = '100px';
    //console.log(dateLabels)
    
    // Create empty asset mix chart
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: price_data["date"],
            datasets: []
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'DD'
                    },
                    ticks: {
                        maxTicksLimit: 4, // Set the maximum number of x-axis labels
                        maxRotation: 0,   // Set the maximum label rotation angle
                        minRotation: 0,
                        align: 'start',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },  
                    },
                    grid: {
                        tickColor: 'rgba(255, 255, 255, 1)'
                    },
                },
                y: {
                    beginAtZero: true,
                    position: 'right',
                    ticks: {
                        // You can add additional y-axis tick options here if needed
                        maxTicksLimit: 3, // Set the maximum number of x-axis labels
                        includeBounds: true,
                        crossAlign: 'far',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },  
                    },
                    grid: {
                        tickColor: 'rgba(255, 255, 255, 1)'
                    },
                },
            },
            animation: false,
            
            plugins: {
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 1)',
                    titleColor: 'rgba(0, 0, 0, 1)',
                    bodyColor: 'rgba(0, 0, 0, 1)',
                    padding: 12,
                    cornerRadius: 12,
                    caretPadding: 12,
                    caretSize: 8,
                    bodyAlign: 'right'
                },
                legend: {
                    responsive: true,
                    display: true,
                    position: 'bottom', // or 'bottom', 'left', 'right'
                    align: 'center', // or 'start', 'end'
                    labels: {
                        font: {
                            size: 12,
                            weight: 'bold',
                        },
                        boxHeight: 2, // Adjust the width of the colored boxes in the legend
                        boxWidth: 20,
                        padding: 15, // Adjust the padding between legend elements
                    },
                },
            },
            
        }
    });
    
    colours = ['rgba(100, 220, 150, 1)', 'rgba(255, 165, 0, 1)', 'rgba(0, 123, 255, 1)', 'rgba(76, 169, 255, 143)', 'rgba(56, 122, 122, 1)', 'rgba(122, 32, 190, 1)']
    
    // Populate asset mix chart
    var count = 0;
    for (var key in price_data) {
        if (price_data.hasOwnProperty(key) && key !== "date") {
            myLineChart.data.datasets.push({
                label: key,
                data: price_data[key],
                fill: false,
                borderColor: colours[count%colours.length],
                borderWidth: 2.5,
                pointRadius: 10,
                pointBorderColor: 'rgba(100, 220, 150, 0)',
                pointBackgroundColor: 'rgba(100, 220, 150, 0)',
                pointHoverRadius: 10,
                pointHoverBackgroundColor: colours[count%colours.length],
                pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
                pointHoverBorderWidth: 3,
            });
            count++;
        }
    } 
    myLineChart.update();
    
    // create charts for each asset
    var assets = {{ portfolio.asset_data|safe }}
    var collapseBuy = {}
    var collapseSell = {}
    
    for (var asset of assets) {
        console.log("asset:", asset.ticker);
        
        console.log("asset.index:", asset.index);
        if (asset.ticker !== "Cash Balance") {
            
            // create chooti chart
            var ctxAssetChart = document.getElementById("asset_chart_" + asset.index).getContext('2d');
            ctxAssetChart.canvas.width = '200px';
            ctxAssetChart.canvas.height = '50px';
            
            if (asset.current_price_change_status === "NEGATIVE") {
                price_chart_border_color = RED_BORDER;
                price_chart_background_color = RED_BACKGROUND;
            } else {
                price_chart_border_color = GREEN_BORDER;
                price_chart_background_color = GREEN_BACKGROUND;
            }
            
            var price_chart_date = JSON.parse(asset.price_chart).date
            var price_chart_price = JSON.parse(asset.price_chart).price
            
            var assetChart = new Chart(ctxAssetChart, {
                type: 'line',
                data: {
                    labels: price_chart_date,
                    datasets: [{
                        data: price_chart_price,
                        fill: true,
                        backgroundColor: price_chart_background_color,
                        borderColor: price_chart_border_color,
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 0,
                    }]              },
                    options: {
                        scales: {
                            x: {
                                display: false,
                                type: 'time',
                                time: {
                                    unit: 'day',
                                    tooltipFormat: 'DD'
                                },
                                grid: {
                                    display: false, // Turn off x-axis grid lines
                                },
                                
                                ticks: {
                                    display: false
                                },
                                scaleLineColor: 'rgba(0, 0, 0, 0)'
                                
                            },
                            y: {
                                display: false,
                                beginAtZero: false,
                                position: 'right',
                                grid: {
                                    display: false, // Turn off x-axis grid lines
                                },
                                
                                ticks: {
                                    display: false
                                },
                                scaleLineColor: 'rgba(0, 0, 0, 0)'
                            }
                        },
                        plugins: {
                            tooltip: {
                                enabled: false,
                                displayColors: false,
                                backgroundColor: 'rgba(255, 255, 255, 1)',
                                titleColor: 'rgba(0, 0, 0, 1)',
                                bodyColor: 'rgba(0, 0, 0, 1)',
                                padding: 12,
                                cornerRadius: 12,
                                caretPadding: 12,
                                caretSize: 8 ,
                                bodyAlign: 'right'                       
                            },
                            hover: {mode: null},
                            legend: {
                                display: false
                            },
                            chartAreaBorder: {
                                borderColor: 'red',
                                borderWidth: 2,
                                borderDash: [5, 5],
                                borderDashOffset: 2,
                            }
                        }
                    }
                });
                
                
                var ctxPriceChart = document.getElementById("price_chart_" + asset.index).getContext('2d');
                ctxPriceChart.canvas.width = '898px';
                ctxPriceChart.canvas.height = '150px';
                
                var myLineChart = new Chart(ctxPriceChart, {
                    type: 'line',
                    data: {
                        labels: price_chart_date,
                        datasets: [{
                            data: price_chart_price,
                            fill: true,
                            backgroundColor: price_chart_background_color,
                            borderColor: price_chart_border_color,
                            borderWidth: 3,
                            pointRadius: 10,
                            pointBorderColor: 'rgba(100, 220, 150, 0)',
                            pointBackgroundColor: 'rgba(100, 220, 150, 0)',
                            pointHoverRadius: 10,
                            pointHoverBackgroundColor: price_chart_border_color,
                            pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
                            pointHoverBorderWidth: 3,
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'day',
                                    tooltipFormat: 'DD'
                                },
                                ticks: {
                                    maxTicksLimit: 4, // Set the maximum number of x-axis labels
                                    maxRotation: 0,   // Set the maximum label rotation angle
                                    minRotation: 0,
                                    align: 'start',
                                    font: {
                                        size: 14,
                                        weight: 'bold'
                                    },  
                                },
                                grid: {
                                    tickColor: 'rgba(255, 255, 255, 1)'
                                },
                            },
                            y: {
                                beginAtZero: false,
                                position: 'right',
                                ticks: {
                                    // You can add additional y-axis tick options here if needed
                                    maxTicksLimit: 4, // Set the maximum number of x-axis labels
                                    includeBounds: true,
                                    crossAlign: 'far',
                                    font: {
                                        size: 14,
                                        weight: 'bold'
                                    },  
                                },
                                grid: {
                                    tickColor: 'rgba(255, 255, 255, 1)'
                                },
                            }
                        },
                        animation: false,
                        tooltips: {
                            mode: 'index',
                            intersect: false
                        },
                        hover: {
                            mode: 'index',
                            intersect: false
                        },
                        plugins: {
                            legend: {
                                display: false,
                            },
                            tooltip: {
                                displayColors: false,
                                backgroundColor: 'rgba(255, 255, 255, 1)',
                                titleColor: 'rgba(0, 0, 0, 1)',
                                bodyColor: 'rgba(0, 0, 0, 1)',
                                padding: 12,
                                cornerRadius: 12,
                                caretPadding: 12,
                                caretSize: 8,
                                bodyAlign: 'right'                      },
                            }
                        }
                    });
                    
                    // create candlestick chart
                    console.log("making cnadlestick chart for", asset.index);
                    var myDiv = document.getElementById("asset_chart_two_" + asset.index).getContext('2d');
                    console.log("myDiv", myDiv);
                    
                    var chart = new Chart(myDiv, {
                        type: 'candlestick',
                        data: {
                            datasets: [{
                                label: asset.ticker,
                                data: [],
                                pointBackgroundColor: 'white',
                                pointBorderColor: 'white',
                                pointBorderWidth: 0,
                                // Custom colors for bullish and bearish candlesticks
                                backgroundColor: {
                                    up: '#111111', // color for rising prices
                                    down: RED_BACKGROUND  // color for falling prices
                                },
                            }]
                        },
                        options: {
                            scales: {
                                x: {
                                    time: {
                                        unit: 'day',
                                        tooltipFormat: 'DD'
                                    },
                                    ticks: {
                                        align: "start",
                                        font: {
                                            size: 14,
                                            weight: 'bold'
                                        },
                                    },
                                    grid: {
                                        tickColor: 'rgba(255, 255, 255, 1)'
                                    },
                                },
                                y: {
                                    beginAtZero: false,
                                    position: 'right',
                                    ticks: {
                                        font: {
                                            size: 14,
                                            weight: 'bold'
                                        }
                                    },
                                    grid: {
                                        tickColor: 'rgba(255, 255, 255, 1)'
                                    },
                                }
                            },
                            plugins: {
                                legend: {
                                    display: false
                                },
                                tooltip: {
                                    displayColors: false,
                                    backgroundColor: 'rgba(255, 255, 255, 1)',
                                    titleColor: 'rgba(0, 0, 0, 1)',
                                    bodyColor: 'rgba(0, 0, 0, 1)',
                                    padding: 12,
                                    cornerRadius: 12,
                                    caretPadding: 12,
                                    bodyAlign: 'right'
                                },
                            },
                            grid: {
                                color: 'rgba(0,0,0,0.1)',
                            },
                            // Add border to the entire chart
                            elements: {
                                line: {
                                    tension: 0, // Disable bezier curves for line chart
                                },
                            },
                            borderColor: 'rgba(0, 0, 0, 1)', // Border color for the entire chart
                            borderWidth: 1, // Border width for the entire chart
                            animation: false, // Disable chart animation
                        }
                    });
                    
                    load_chart(asset.ticker, asset.index,'threeM', chart);
                    var index = String(asset.index)
                    var collapseBuyItem = new bootstrap.Collapse(document.getElementById("collapseBuy_" + index));
                    var collapseSellItem = new bootstrap.Collapse(document.getElementById("collapseSell_" + index));
                    //collapseBuyItem.hide()
                    //collapseSellItem.hide()
                    console.log("hiding", collapseBuyItem)
                    console.log("hiding", collapseSellItem)
                    
                    
                    collapseBuy[index] = collapseBuyItem
                    collapseSell[index] = collapseSellItem
                    
                    console.log("added", asset.index, "to", collapseBuy)
                    console.log("added", asset.index, "to", collapseSell)
                    
                    document.getElementById("buy-order-button_" + index).addEventListener('change', function (event) {
                        // Before showing the first collapse, ensure the second one is closed
                        var checkBox = event.target
                        //document.getElementById('collapseOrder_' + checkBox.dataset.index).style.display = "block";
                        //collapseBuy[checkBox.dataset.index].show();
                        
                        //checkBox.classList.add("collapsed")
                        console.log("running collapse listener to ", event.target, "supposed to trigger hide for", checkBox.dataset.index)
                        //event.target.checked = true
                        document.getElementById("sell-order-button_" + checkBox.dataset.index).checked = false
                        collapseSell[checkBox.dataset.index].hide();
                    });
                    
                    document.getElementById("sell-order-button_" + index).addEventListener('change', function (event) {
                        // Before showing the second collapse, ensure the first one is closed
                        //collapseSell[checkBox.dataset.index].show();
                        
                        var checkBox = event.target
                        //document.getElementById('collapseOrder_' + checkBox.dataset.index).style.display = "block";
                        //checkBox.classList.remove("collapsed")
                        console.log("running collapse listener to ", event.target, "supposed to trigger hide for", checkBox.dataset.index)
                        
                        //event.target.checked = true
                        
                        document.getElementById("buy-order-button_" + checkBox.dataset.index).checked = false
                        collapseBuy[checkBox.dataset.index].hide();
                        
                    });
                    
                    
                    
                    document.getElementById("buy-num-units_" + asset.index).addEventListener("keyup", function(event) {
                        // Check if the "Enter" key (key code 13) was pressed
                        var content = "USD 0.00"
                        
                        try {
                            var index = event.target.dataset.index
                            var price = parseFloat(event.target.dataset.price)
                            var str = event.target.value
                            console.log("str is", str)
                            
                            if (hasTwoOrFewerDecimalPoints(str)) {
                                var units = parseFloat(str)
                                console.log("units is", units)
                                console.log("current_price is", price)
                                
                                var currentPriceUsdDiv = document.getElementById('buy-current-price-usd_' + index);
                                
                                console.log("currentPriceUsdDiv", currentPriceUsdDiv)
                                if (currentPriceUsdDiv) {
                                    console.log(currentPriceUsdDiv.dataset.value)
                                    const currentPriceUsd = parseFloat(currentPriceUsdDiv.dataset.value)
                                    console.log("read price usd as", currentPriceUsd)
                                    var total = units * currentPriceUsd
                                } else {
                                    var total = units * price
                                }
                                
                                total = total.toFixed(2)
                                console.log("total is", total)
                                console.log("buy-order-value_" + index)
                                
                                content = "USD " + total
                                if (total > parseFloat("{{ portfolio.cash_balance }}")) {
                                    triggerBuyNotAdequateCashMessage(index)
                                }  else if (units > 0) {
                                    triggerBuyValidMessage(index)
                                } else {
                                    deleteBuyMessages(index)
                                }
                            } else {
                                if (str !== "") {
                                    triggerBuyMultiplesMessage(index)
                                    console.log("has to be multiples of 0.01")
                                } else {
                                    deleteBuyMessages(index)
                                }
                            }
                        } catch (error) {
                            // Handle the error here if needed
                            console.error("An error occurred:", error);
                        }
                        document.getElementById("buy-order-value_" + index).innerHTML = content
                    });
                    
                    document.getElementById("sell-num-units_" + asset.index).addEventListener("keyup", function(event) {
                        // Check if the "Enter" key (key code 13) was pressed
                        var content = "USD 0.00"
                        
                        try {
                            var index = event.target.dataset.index
                            var price = parseFloat(event.target.dataset.price)
                            var current_units = parseFloat(event.target.dataset.current_units)
                            var str = event.target.value
                            console.log("str is", str)
                            console.log("current_units is", current_units)
                            
                            
                            if (hasTwoOrFewerDecimalPoints(str)) {
                                var units = parseFloat(str)
                                console.log("units is", units)
                                console.log("current_price is", price)
                                
                                var currentPriceUsdDiv = document.getElementById('sell-current-price-usd_' + index);
                                
                                console.log("currentPriceUsdDiv", currentPriceUsdDiv)
                                if (currentPriceUsdDiv) {
                                    console.log(currentPriceUsdDiv.dataset.value)
                                    const currentPriceUsd = parseFloat(currentPriceUsdDiv.dataset.value)
                                    console.log("read price usd as", currentPriceUsd)
                                    var total = units * currentPriceUsd
                                } else {
                                    var total = units * price
                                }
                                
                                total = total.toFixed(2)
                                console.log("total is", total)
                                console.log("sell-order-value_" + index)
                                
                                content = "USD " + total
                                if (units > current_units) {
                                    triggerSellNotAdequateUnitsMessage(index)
                                } else if (units > 0) {
                                    triggerSellValidMessage(index)
                                } else {
                                    deleteSellMessages(index)
                                }
                            } else {
                                if (str !== "") {
                                    triggerSellMultiplesMessage(index)
                                } else {
                                    deleteSellMessages(index)
                                }
                            }
                        } catch (error) {
                            // Handle the error here if needed
                            console.error("An error occurred:", error);
                        }
                        document.getElementById("sell-order-value_" + index).innerHTML = content
                    });
                    
                    
                    
                    
                    
                    
                    
                    //document.querySelectorAll('.btn-check').forEach(function (checkbox) {
                    //  checkbox.addEventListener('change', function (event) {
                    //    var checkBox = event.target;
                    //
                    //    if (checkBox.checked) {
                    //      // If a checkbox is checked, hide the other collapse
                    //      if (checkBox.id.includes('buy-order-button')) {
                    //        collapseSell['collapseSell_' + checkBox.dataset.index].hide();
                    //      } else if (checkBox.id.includes('sell-order-button')) {
                    //        collapseBuy['collapseBuy_' + checkBox.dataset.index].hide();
                    //      }
                    //    }
                    //  });
                    //});
                    
                    
                    //document.getElementById("buy-order-button_" + index).click()
                    //document.getElementById("sell-order-button_" + index).click()
                    
                    //collapseBuy[index].hide()
                    //collapseSell[index].hide()
                }
            }
            
            // create chooti chart for search asset
            var ctxSearchAssetChart = document.getElementById("search_asset_small_chart").getContext('2d');
            ctxSearchAssetChart.canvas.width = '200px';
            ctxSearchAssetChart.canvas.height = '50px';
            
            
            var searchAssetChart = new Chart(ctxSearchAssetChart, {
                type: 'line',
                data: {
                    labels: price_chart_date,
                    datasets: []              },
                    options: {
                        scales: {
                            x: {
                                display: false,
                                type: 'time',
                                time: {
                                    unit: 'day',
                                    tooltipFormat: 'DD'
                                },
                                grid: {
                                    display: false, // Turn off x-axis grid lines
                                },
                                
                                ticks: {
                                    display: false
                                },
                                scaleLineColor: 'rgba(0, 0, 0, 0)'
                                
                            },
                            y: {
                                display: false,
                                beginAtZero: false,
                                position: 'right',
                                grid: {
                                    display: false, // Turn off x-axis grid lines
                                },
                                
                                ticks: {
                                    display: false
                                },
                                scaleLineColor: 'rgba(0, 0, 0, 0)'
                            }
                        },
                        plugins: {
                            tooltip: {
                                enabled: false,
                                displayColors: false,
                                backgroundColor: 'rgba(255, 255, 255, 1)',
                                titleColor: 'rgba(0, 0, 0, 1)',
                                bodyColor: 'rgba(0, 0, 0, 1)',
                                padding: 12,
                                cornerRadius: 12,
                                caretPadding: 12,
                                caretSize: 8 ,
                                bodyAlign: 'right'                       
                            },
                            hover: {mode: null},
                            legend: {
                                display: false
                            },
                            chartAreaBorder: {
                                borderColor: 'red',
                                borderWidth: 2,
                                borderDash: [5, 5],
                                borderDashOffset: 2,
                            }
                        }
                    }
                });
                
                var ctxSearchAssetPriceChart = document.getElementById("search_asset_price_chart").getContext('2d');
                ctxSearchAssetPriceChart.canvas.width = '898px';
                ctxSearchAssetPriceChart.canvas.height = '150px';
                
                var searchAssetPriceChart = new Chart(ctxSearchAssetPriceChart, {
                    type: 'line',
                    data: {
                        datasets: []
                    },
                    options: {
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'day',
                                    tooltipFormat: 'DD'
                                },
                                ticks: {
                                    maxTicksLimit: 4, // Set the maximum number of x-axis labels
                                    maxRotation: 0,   // Set the maximum label rotation angle
                                    minRotation: 0,
                                    align: 'start',
                                    font: {
                                        size: 14,
                                        weight: 'bold'
                                    },  
                                },
                                grid: {
                                    tickColor: 'rgba(255, 255, 255, 1)'
                                },
                            },
                            y: {
                                beginAtZero: false,
                                position: 'right',
                                ticks: {
                                    // You can add additional y-axis tick options here if needed
                                    maxTicksLimit: 4, // Set the maximum number of x-axis labels
                                    includeBounds: true,
                                    crossAlign: 'far',
                                    font: {
                                        size: 14,
                                        weight: 'bold'
                                    },  
                                },
                                grid: {
                                    tickColor: 'rgba(255, 255, 255, 1)'
                                },
                            }
                        },
                        animation: false,
                        tooltips: {
                            mode: 'index',
                            intersect: false
                        },
                        hover: {
                            mode: 'index',
                            intersect: false
                        },
                        plugins: {
                            legend: {
                                display: false,
                            },
                            tooltip: {
                                displayColors: false,
                                backgroundColor: 'rgba(255, 255, 255, 1)',
                                titleColor: 'rgba(0, 0, 0, 1)',
                                bodyColor: 'rgba(0, 0, 0, 1)',
                                padding: 12,
                                cornerRadius: 12,
                                caretPadding: 12,
                                caretSize: 8,
                                bodyAlign: 'right'                      },
                            }
                        }
                    });
                    
                    // create candlestick chart
                    console.log("making cnadlestick chart for search asset");
                    var myDiv = document.getElementById("asset_chart_two_" + "search_asset").getContext('2d');
                    console.log("myDiv", myDiv);
                    
                    var candlestickSearchAssetChart = new Chart(myDiv, {
                        type: 'candlestick',
                        data: {
                            datasets: [{
                                label: asset.ticker,
                                data: [],
                                pointBackgroundColor: 'white',
                                pointBorderColor: 'white',
                                pointBorderWidth: 0,
                                // Custom colors for bullish and bearish candlesticks
                                backgroundColor: {
                                    up: '#111111', // color for rising prices
                                    down: RED_BACKGROUND  // color for falling prices
                                },
                            }]
                        },
                        options: {
                            scales: {
                                x: {
                                    time: {
                                        unit: 'day',
                                        tooltipFormat: 'DD'
                                    },
                                    ticks: {
                                        align: "start",
                                        font: {
                                            size: 14,
                                            weight: 'bold'
                                        },
                                    },
                                    grid: {
                                        tickColor: 'rgba(255, 255, 255, 1)'
                                    },
                                },
                                y: {
                                    beginAtZero: false,
                                    position: 'right',
                                    ticks: {
                                        font: {
                                            size: 14,
                                            weight: 'bold'
                                        }
                                    },
                                    grid: {
                                        tickColor: 'rgba(255, 255, 255, 1)'
                                    },
                                }
                            },
                            plugins: {
                                legend: {
                                    display: false
                                },
                                tooltip: {
                                    displayColors: false,
                                    backgroundColor: 'rgba(255, 255, 255, 1)',
                                    titleColor: 'rgba(0, 0, 0, 1)',
                                    bodyColor: 'rgba(0, 0, 0, 1)',
                                    padding: 12,
                                    cornerRadius: 12,
                                    caretPadding: 12,
                                    bodyAlign: 'right'
                                },
                            },
                            grid: {
                                color: 'rgba(0,0,0,0.1)',
                            },
                            // Add border to the entire chart
                            elements: {
                                line: {
                                    tension: 0, // Disable bezier curves for line chart
                                },
                            },
                            borderColor: 'rgba(0, 0, 0, 1)', // Border color for the entire chart
                            borderWidth: 1, // Border width for the entire chart
                            animation: false, // Disable chart animation
                        }
                    });
                    
                    
                    
                    function load_chart(ticker, index, width, chart) {
                        var myDiv = document.getElementById("asset_chart_two_" + index);
                        myDiv.style.display = 'none';
                        var myDiv = document.getElementById('asset_chart_spinner_' + index);
                        myDiv.classList.remove('d-none');
                        
                        console.log("running load_chart on", ticker, width);
                        fetch('{{ portfolio.id }}' + '/asset_data', {
                            method: 'POST',
                            body: JSON.stringify({
                                ticker: ticker,
                                width: width
                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            // Print result
                            var myDiv = document.getElementById("asset_chart_two_" + index);
                            myDiv.style.display = '';
                            var myDiv = document.getElementById('asset_chart_spinner_' + index);
                            myDiv.classList.add('d-none');
                            
                            console.log(result);
                            var chartData = result.chart_data;
                            chart.data.datasets[0].data = chartData;
                            chart.update();
                            
                            
                        })
                    }
                    
                    
                    
                    function search_asset() {
                        ticker = document.getElementById("search_ticker").value;
                        if (ticker.trim() === "") {
                            return
                        }
                        console.log("search_ticker:", ticker)
                        
                        var myDiv = document.getElementById("search_asset_data");
                        myDiv.style.display = 'none';
                        var myDiv = document.getElementById('search_asset_spinner');
                        myDiv.classList.remove('d-none');
                        
                        fetch('{{ portfolio.id }}' + '/search_asset', {
                            method: 'POST',
                            body: JSON.stringify({
                                ticker: ticker
                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            console.log(result)
                            
                            // Update info
                            
                            document.getElementById("search_asset_ticker").innerHTML = result.ticker;
                            document.getElementById("search_asset_long_name").innerHTML = result.long_name;
                            document.getElementById("search_asset_price").innerHTML = result.current_price;
                            change_button = document.getElementById("search_asset_price_change")
                            change_button.innerHTML =  result.current_price_change;
                            
                            change_button.classList.remove(...change_button.classList);
                            change_button.classList.add("badge")
                            if (result.current_price_change_status === "POSITIVE") {
                                change_button.classList.add("text-bg-success")
                                
                            } else if (result.current_price_change_status === "ZERO") {
                                change_button.classList.add("text-bg-light")
                                
                            } else if (result.current_price_change_status === "NEGATIVE") {
                                change_button.classList.add("text-bg-danger")
                                
                            }
                            
                            /*
                            result.country
                            result.quote_type
                            result.currency
                            result.exchange
                            result.long_business_summary
                            result.current_price_change_status
                            result.dollar_price
                            */
                            
                            document.getElementById("search_asset_currency").innerHTML = result.currency;
                            document.getElementById("search_asset_country").innerHTML = result.country;
                            document.getElementById("search_asset_quote_type").innerHTML = result.quote_type;
                            document.getElementById("search_asset_exchange").innerHTML = result.exchange;
                            document.getElementById("search_asset_summary").innerHTML = result.long_business_summary;
                            
                            
                            
                            if (result.current_price_change_status === "NEGATIVE") {
                                price_chart_border_color = RED_BORDER;
                                price_chart_background_color = RED_BACKGROUND;
                            } else {
                                price_chart_border_color = GREEN_BORDER;
                                price_chart_background_color = GREEN_BACKGROUND;
                            }
                            
                            var price_chart_date = JSON.parse(result.price_chart).date;
                            var price_chart_price = JSON.parse(result.price_chart).price;
                            
                            console.log(price_chart_date, price_chart_price);
                            
                            var chartData = result.chart_data;
                            searchAssetChart.data.labels = price_chart_date;
                            searchAssetChart.data.datasets[0] = {
                                data: price_chart_price,
                                fill: true,
                                backgroundColor: price_chart_background_color,
                                borderColor: price_chart_border_color,
                                borderWidth: 2.5,
                                pointRadius: 0,
                                pointHoverRadius: 0,
                            }
                            
                            searchAssetChart.update();
                            
                            searchAssetPriceChart.data.labels = price_chart_date;
                            searchAssetPriceChart.data.datasets[0] = {
                                data: price_chart_price,
                                fill: true,
                                backgroundColor: price_chart_background_color,
                                borderColor: price_chart_border_color,
                                borderWidth: 3,
                                pointRadius: 10,
                                pointBorderColor: 'rgba(100, 220, 150, 0)',
                                pointBackgroundColor: 'rgba(100, 220, 150, 0)',
                                pointHoverRadius: 10,
                                pointHoverBackgroundColor: price_chart_border_color,
                                pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
                                pointHoverBorderWidth: 3,
                            }
                            
                            searchAssetPriceChart.update();
                            load_chart(result.ticker, "search_asset",'threeM', candlestickSearchAssetChart);
                            var myDiv = document.getElementById('search_asset_spinner');
                            myDiv.classList.add('d-none');
                            var myDiv = document.getElementById("search_asset_data");
                            myDiv.style.display = '';
                            document.getElementById("buy-num-units_search_asset").value = ""
                            
                            document.getElementById("buy-order-value_search_asset").innerHTML = "USD 0.00"
                            document.getElementById("buy_search_asset_display").innerHTML = result.ticker
                            document.getElementById("buy_search_asset_input").value = result.ticker
                            document.getElementById("buy_search_asset_price").innerHTML = result.currency + " " + result.current_price
                            deleteBuyMessages("search_asset")
                            
                            if (result.currency !== "USD") {
                                document.getElementById("buy-rate-container_search_asset").style.display = 'flex'
                                document.getElementById("buy-current-price-usd_search_asset").innerHTML = 'USD ' + result.current_price_usd.toFixed(2);
                                document.getElementById("buy-num-units_search_asset").dataset.price = String(result.current_price_usd)
                                
                            } else {
                                document.getElementById("buy-rate-container_search_asset").style.display = 'none'
                                document.getElementById("buy-current-price-usd_search_asset").innerHTML = ''
                                document.getElementById("buy-num-units_search_asset").dataset.price = String(result.current_price)
                            }
                            
                        })
                    }
                    
                    var searchButton = document.getElementById("search_trigger");
                    
                    // Add an event listener to the button and attach the search_asset function
                    searchButton.addEventListener("click", search_asset);
                    
                    var searchInput = document.getElementById("search_ticker");
                    // Add an event listener for the "keyup" event
                    searchInput.addEventListener("keyup", function(event) {
                        // Check if the "Enter" key (key code 13) was pressed
                        if (event.key === "Enter") {
                            // Call the search_asset function when "Enter" is pressed
                            search_asset();
                        }
                    });
                    
                    
                    
                    // Assuming you are using Bootstrap's data-bs-target attribute to identify the accordion element
                    document.getElementById('showAllButton').addEventListener('click', function() {
                        console.log("showAllButton clicked...")
                        var accordionButtons = document.querySelectorAll('.accordion-button.collapsed');
                        console.log("collapsed buttons", accordionButtons)
                        accordionButtons.forEach(button => button.click())
                    });
                    
                    document.getElementById('collapseAllButton').addEventListener('click', function() {
                        console.log("collapseAllButton clicked...")
                        
                        var accordionButtons = document.querySelectorAll('.accordion-button:not(.collapsed)');
                        console.log("non collapsed buttons", accordionButtons)
                        
                        accordionButtons.forEach(button => button.click())
                    });
                });
                
                
                function dropAssets() {
                    var elements = document.getElementsByClassName("accordion-collapse");
                    var elementsArray = Array.from(elements);
                    
                    // Remove class from each element
                    elementsArray.forEach(function(element) {
                        element.classList.add("show");
                        //element.aria-expanded="true";
                    });
                }
                
                function collapseAssets() {
                    var elements = document.getElementsByClassName("accordion-collapse");
                    var elementsArray = Array.from(elements);
                    
                    // Remove class from each element
                    elementsArray.forEach(function(element) {
                        element.classList.remove("show");
                        //element.aria-expanded="false";
                    });
                }
                
                function addMessage(content, type) {
                    const chatContainer = document.getElementById('chat-container');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message ' + type;
                    chatContainer.appendChild(messageDiv);
                    
                    // Split the content into words
                    const words = content.split(' ');
                    
                    words.forEach((word, index) => {
                        setTimeout(() => {
                            if (index !== 0) {
                                messageDiv.innerHTML = messageDiv.textContent.slice(0, -2);
                            }
                            messageDiv.innerHTML += word;
                            if (words[index+1] !== undefined) {
                                messageDiv.innerHTML += ' ' + '  ●';
                            }
                        }, (index * 200) + 200*Math.random()); // Adjust the delay as needed (500 milliseconds in this example)
                    });
                }
                
                function tickOneDay() {
                    // Change the location of the current page to the specified URL
                    window.location.href = "{% url 'tick_one_day' portfolio.id %}";
                }
                
                
                function openInNewTab(url) {
                    var win = window.open(url, '_blank');
                    win.focus();
                }
                
                // Example usage:
                addMessage("{{ portfolio.advice }}", "bot_message");
                //document.getElementById("article_0").classList.add("active");
                
                
                function hasTwoOrFewerDecimalPoints(str) {
                    // Regular expression to match integers or floats with two or fewer decimal points
                    const regex = /^\d+(\.\d{0,2})?$/;
                    
                    // Test if the string matches the regular expression
                    return regex.test(str);
                }
                
                function triggerBuyNotAdequateCashMessage(index) {
                    document.getElementById('buy-num-units_'+ index + 'InvalidFeedback').innerHTML = "Not adequate cash."
                    document.getElementById('buy-num-units_'+ index).classList.remove("is-valid")
                    document.getElementById('buy-num-units_'+ index).classList.add("is-invalid")
                    document.getElementById('placeBuyOrder_'+ index).disabled = true;
                }
                
                
                function triggerBuyMultiplesMessage(index) {
                    document.getElementById('buy-num-units_'+ index + 'InvalidFeedback').innerHTML = "Enter multiple of 0.01"
                    document.getElementById('buy-num-units_'+ index).classList.remove("is-valid")
                    document.getElementById('buy-num-units_'+ index).classList.add("is-invalid")
                    document.getElementById('placeBuyOrder_'+ index).disabled = true;
                    
                }
                
                function triggerBuyValidMessage(index) {
                    document.getElementById('buy-num-units_'+ index).classList.remove("is-invalid")
                    document.getElementById('buy-num-units_'+ index).classList.add("is-valid")
                    document.getElementById('placeBuyOrder_'+ index).disabled = false;
                }
                
                function deleteBuyMessages(index) {
                    document.getElementById('buy-num-units_'+ index).classList.remove("is-invalid")
                    document.getElementById('buy-num-units_'+ index).classList.remove("is-valid")
                    document.getElementById('placeBuyOrder_'+ index).disabled = false;
                }
                
                function triggerSellNotAdequateUnitsMessage(index) {
                    document.getElementById('sell-num-units_'+ index + 'InvalidFeedback').innerHTML = "Not adequate units!"
                    document.getElementById('sell-num-units_'+ index).classList.remove("is-valid")
                    document.getElementById('sell-num-units_'+ index).classList.add("is-invalid")
                    document.getElementById('placeSellOrder_'+ index).disabled = true;
                }
                
                function triggerSellMultiplesMessage(index) {
                    document.getElementById('sell-num-units_'+ index + 'InvalidFeedback').innerHTML = "Enter multiple of 0.01!"
                    document.getElementById('sell-num-units_'+ index).classList.remove("is-valid")
                    document.getElementById('sell-num-units_'+ index).classList.add("is-invalid")
                    document.getElementById('placeSellOrder_'+ index).disabled = true;
                }
                
                function triggerSellValidMessage(index) {
                    document.getElementById('sell-num-units_'+ index).classList.remove("is-invalid")
                    document.getElementById('sell-num-units_'+ index).classList.add("is-valid")
                    document.getElementById('placeSellOrder_'+ index).disabled = false;
                }
                
                function deleteSellMessages(index) {
                    document.getElementById('sell-num-units_'+ index).classList.remove("is-invalid")
                    document.getElementById('sell-num-units_'+ index).classList.remove("is-valid")
                    document.getElementById('placeSellOrder_'+ index).disabled = false;
                }
                
                document.getElementById("buy-num-units_search_asset").addEventListener("keyup", function(event) {
                    // Check if the "Enter" key (key code 13) was pressed
                    var content = "USD 0.00"
                    
                    try {
                        var index = "search_asset"
                        var price = parseFloat(event.target.dataset.price)
                        var str = event.target.value
                        console.log("str is", str)
                        
                        if (hasTwoOrFewerDecimalPoints(str)) {
                            var units = parseFloat(str)
                            console.log("units is", units)
                            console.log("current_price is", price)
                            
                            var total = units * price
                            total = total.toFixed(2)
                            console.log("total is", total)
                            console.log("buy-order-value_" + index)
                            
                            content = "USD " + total
                            if (total > parseFloat("{{ portfolio.cash_balance }}")) {
                                triggerBuyNotAdequateCashMessage(index)
                            }  else if (units > 0) {
                                triggerBuyValidMessage(index)
                            } else {
                                deleteBuyMessages(index)
                            }
                        } else {
                            if (str !== "") {
                                triggerBuyMultiplesMessage(index)
                                console.log("has to be multiples of 0.01")
                            } else {
                                deleteBuyMessages(index)
                            }
                        }
                    } catch (error) {
                        // Handle the error here if needed
                        console.error("An error occurred:", error);
                    }
                    document.getElementById("buy-order-value_search_asset").innerHTML = content
                    
                })
                function closePortfolio() {
                    window.location.href = "{% url 'close_portfolio' portfolio.id %}";
                }
                
                function archivePortfolio() {
                    window.location.href = "{% url 'archive_portfolio' portfolio.id %}";
                }
                
                function unarchivePortfolio() {
                    window.location.href = "{% url 'unarchive_portfolio' portfolio.id %}";
                }
                
                