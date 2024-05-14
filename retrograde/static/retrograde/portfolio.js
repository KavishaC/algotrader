//import { CHART_COLOURS, assetMixColours, portfolioValueChartConfig, assetMixChartConfig, smallAssetChartConfig, assetPriceChartConfig, assetCandlestickChartConfig } from './portfolioCharts.js';

var collapseBuy = {}
var collapseSell = {}

document.addEventListener('DOMContentLoaded', function () {
    addMessage();
    addNews()
    createPortfolioValueChart()
    createAssetMixChart()
    
    // Create charts for each asset
    for (var asset of assets) {
        //console.log("asset:", asset.index, asset.ticker);
        if (asset.ticker !== "Cash Balance") {
            createSmallAssetPriceChart(asset)
            createAssetPriceChart(asset)
            createCandlestickChart(asset)
            createBetaChart(asset)
            createBuySellContainers(asset)
        }
    }
    load_search_asset_charts()
});

function createPortfolioValueChart() {
    // Create portfolio value chart
    var ctx = document.getElementById('assetValue').getContext('2d');
    ctx.canvas.width = '898px';
    ctx.canvas.height = '150px';
    
    var borderColor;
    var backgroundColor;
    // Determine colors of value chart
    if (portfolioChangeStatus === "NEGATIVE") {
        borderColor = CHART_COLOURS.RED_BORDER;
        backgroundColor = CHART_COLOURS.RED_BACKGROUND;
        backgroundColorGrad = CHART_COLOURS.RED_BACKGROUND_GRAD;
        backgroundColorGradLow = CHART_COLOURS.RED_BACKGROUND_GRAD_LOW;
    } else {
        borderColor = CHART_COLOURS.GREEN_BORDER;
        backgroundColor = CHART_COLOURS.GREEN_BACKGROUND;
        backgroundColorGrad = CHART_COLOURS.GREEN_BACKGROUND_GRAD;
        backgroundColorGradLow = CHART_COLOURS.GREEN_BACKGROUND_GRAD_LOW;
    }
    
    var portfolioValueChart = new Chart(ctx, portfolioValueChartConfig);
    
    portfolioValueChart.data.datasets[0].borderColor = borderColor;
    portfolioValueChart.data.datasets[0].pointHoverBackgroundColor = borderColor
    portfolioValueChart.data.datasets[0].backgroundColor = (context) => {
        if (!context.chart.chartArea) {
            return;
        }
        
        const { ctx, data, chartArea: {top, bottom} } = context.chart;
        //console.log("top", top, ": bottom", bottom)
        const gradientBg = ctx.createLinearGradient(0, top, 0, bottom);
        gradientBg.addColorStop(1, backgroundColorGradLow)
        gradientBg.addColorStop(0, backgroundColorGrad)
        return gradientBg;
    }
    portfolioValueChart.update();
}

function createAssetMixChart() {
    var ctx = document.getElementById('allocation_chart').getContext('2d');
    ctx.canvas.width = '898px';
    ctx.canvas.height = '100px';
    
    // Create empty asset mix chart
    var assetMixChart = new Chart(ctx, assetMixChartConfig);
    
    // Populate asset mix chart
    var count = 0;
    for (var key in price_data) {
        if (price_data.hasOwnProperty(key) && key !== "date") {
            assetMixChart.data.datasets.push({
                label: key,
                data: price_data[key],
                fill: false,
                borderColor: assetMixColours[count%assetMixColours.length],
                borderWidth: 2.5,
                pointRadius: 10,
                pointBorderColor: 'rgba(100, 220, 150, 0)',
                pointBackgroundColor: 'rgba(100, 220, 150, 0)',
                pointHoverRadius: 10,
                pointHoverBackgroundColor: assetMixColours[count%assetMixColours.length],
                pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
                pointHoverBorderWidth: 3,
            });
            count++;
        }
    } 
    assetMixChart.update();
}

function createSmallAssetPriceChart(asset) {
    //console.log("creating small asset chart for", asset)

    var ctxAssetChart = document.getElementById("asset_chart_" + asset.index).getContext('2d');
    ctxAssetChart.canvas.width = '200px';
    ctxAssetChart.canvas.height = '50px';
    
    var price_chart_border_color;
    var price_chart_background_color;

    if (asset.current_price_change_status === "NEGATIVE") {
            borderColor = CHART_COLOURS.RED_BORDER;
            backgroundColor = CHART_COLOURS.RED_BACKGROUND;
            backgroundColorGrad = CHART_COLOURS.RED_BACKGROUND_GRAD;
            backgroundColorGradLow = CHART_COLOURS.RED_BACKGROUND_GRAD_LOW;
        } else {
            borderColor = CHART_COLOURS.GREEN_BORDER;
            backgroundColor = CHART_COLOURS.GREEN_BACKGROUND;
            backgroundColorGrad = CHART_COLOURS.GREEN_BACKGROUND_GRAD;
            backgroundColorGradLow = CHART_COLOURS.GREEN_BACKGROUND_GRAD_LOW;
        }
    
    var price_chart_date = JSON.parse(asset.price_chart).date
    var price_chart_price = JSON.parse(asset.price_chart).price
    //console.log("last price for", asset.index, "is", price_chart_price)
    
    var smallAssetChart = new Chart(ctxAssetChart, _.cloneDeep(smallAssetChartConfig));
    smallAssetChart.data.labels = price_chart_date;
    smallAssetChart.data.datasets[0].data = price_chart_price;
    smallAssetChart.data.datasets[0].borderColor = borderColor;
    smallAssetChart.data.datasets[0].backgroundColor = (context) => {
        const { ctx, data, chartArea: {top, bottom} } = context.chart;
        //console.log("top", top, ": bottom", bottom)
        const gradientBg = ctx.createLinearGradient(0, top, 0, bottom);
        gradientBg.addColorStop(1, 'rgba(255, 255, 255, 0.3)')
        gradientBg.addColorStop(0, backgroundColorGrad)
        return gradientBg;
    }
    smallAssetChart.update()
}

function createAssetPriceChart(asset) {
    //console.log("creating asset chart for", asset)
    
    var ctxPriceChart = document.getElementById("price_chart_" + asset.index).getContext('2d');
    ctxPriceChart.canvas.width = '898px';
    ctxPriceChart.canvas.height = '150px';
    
    var borderColor;
    var backgroundColor;
    var backgroundColorGrad;
    var backgroundColorGradLow;

    if (asset.current_price_change_status === "NEGATIVE") {
        borderColor = CHART_COLOURS.RED_BORDER;
        backgroundColor = CHART_COLOURS.RED_BACKGROUND;
        backgroundColorGrad = CHART_COLOURS.RED_BACKGROUND_GRAD;
        backgroundColorGradLow = CHART_COLOURS.RED_BACKGROUND_GRAD_LOW;
    } else {
        borderColor = CHART_COLOURS.GREEN_BORDER;
        backgroundColor = CHART_COLOURS.GREEN_BACKGROUND;
        backgroundColorGrad = CHART_COLOURS.GREEN_BACKGROUND_GRAD;
        backgroundColorGradLow = CHART_COLOURS.GREEN_BACKGROUND_GRAD_LOW;
    }
    console.log("backgroundColorGrad for",asset.index, backgroundColorGrad)
    console.log("backgroundColorGradLow for",asset.index, backgroundColorGradLow)

    var price_chart_date = JSON.parse(asset.price_chart).date
    var price_chart_price = JSON.parse(asset.price_chart).price
    //console.log("last price for", asset.index, "is", price_chart_price)
    
    var assetPriceChart = new Chart(ctxPriceChart, _.cloneDeep(assetPriceChartConfig));
    assetPriceChart.data.labels = price_chart_date;
    assetPriceChart.data.datasets[0].data = price_chart_price;
    assetPriceChart.data.datasets[0].borderColor = borderColor;
    assetPriceChart.data.datasets[0].pointHoverBackgroundColor = borderColor;
    assetPriceChart.data.datasets[0].backgroundColor = (context) => {
        const { ctx, data, chartArea: {top, bottom} } = context.chart;
        //console.log("top", top, ": bottom", bottom)
        const gradientBg = ctx.createLinearGradient(0, top, 0, top + 160);
        gradientBg.addColorStop(1, 'rgba(255, 255, 255, 0.3)')
        gradientBg.addColorStop(0, backgroundColorGrad)
        return gradientBg;
    }
    assetPriceChart.update()
}

function createCandlestickChart(asset) {
    //console.log("making candlestick chart for", asset);
    var myDiv = document.getElementById("asset_chart_two_" + asset.index).getContext('2d');
    //console.log("myDiv", myDiv);
    
    var assetCandlestickChart = new Chart(myDiv, _.cloneDeep(assetCandlestickChartConfig));
    assetCandlestickChart.data.datasets[0].label = asset.ticker
    assetCandlestickChart.update()
    
    load_chart(asset.ticker, asset.index,'threeM', assetCandlestickChart);
}

function createBetaChart(asset) {
    //console.log("creating asset chart for", asset)
    
    var ctxBetaChart = document.getElementById("asset_chart_beta_" + asset.index).getContext('2d');
    ctxBetaChart.canvas.width = 350;
    ctxBetaChart.canvas.height = 250;
    
    const scatter_plot_data = asset.beta_chart[0]["scatter_plot_data"];
    const line_plot_data = asset.beta_chart[0]["line_plot_data"];

    //console.log("asset.beta_chart", asset.beta_chart)
    //console.log("line_plot_data", line_plot_data)
    //console.log("scatter_plot_data", scatter_plot_data)

    var data = {
            datasets: [{
                type: 'scatter',
                label: 'Scatter Plot',
                data: scatter_plot_data,
                backgroundColor: 'rgba(75, 192, 192, 0.8)',
            },
            {
                type: 'line',
                label: 'Linear Plot',
                data: line_plot_data,
                borderColor: 'rgba(75, 192, 192, 0.8)',
                borderWidth: 3,
                pointRadius: 0,
                pointHoverRadius: 0,
            }]
        }
    
    var assetBetaChart = new Chart(ctxBetaChart, _.cloneDeep(assetBetaChartConfig));
    assetBetaChart.data = _.cloneDeep(data)
    console.log("assetBetaChart", assetBetaChart)
    assetBetaChart.update()
}

function createBuySellContainers(asset) {
    
    var index = String(asset.index)
    
    var collapseBuyItem = new bootstrap.Collapse(document.getElementById("collapseBuy_" + index));
    var collapseSellItem = new bootstrap.Collapse(document.getElementById("collapseSell_" + index));
    
    collapseBuy[index] = collapseBuyItem
    collapseSell[index] = collapseSellItem
    
    document.getElementById("buy-order-button_" + index).addEventListener('change', function (event) {
        var checkBox = event.target
        //console.log("running collapse listener to ", event.target, "supposed to trigger hide for", checkBox.dataset.index)
        document.getElementById("sell-order-button_" + checkBox.dataset.index).checked = false
        collapseSell[checkBox.dataset.index].hide();
    });
    
    document.getElementById("sell-order-button_" + index).addEventListener('change', function (event) {
        var checkBox = event.target
        //console.log("running collapse listener to ", event.target, "supposed to trigger hide for", checkBox.dataset.index)
        document.getElementById("buy-order-button_" + checkBox.dataset.index).checked = false
        collapseBuy[checkBox.dataset.index].hide();
    });
    
    
    document.getElementById("buy-num-units_" + asset.index).addEventListener("keyup", function(event) {
        var content = "USD 0.00"
        
        try {
            var index = event.target.dataset.index
            var price = parseFloat(event.target.dataset.price)
            var str = event.target.value
            //console.log("str is", str)
            
            if (hasTwoOrFewerDecimalPoints(str)) {
                var units = parseFloat(str)
                //console.log("units is", units)
                //console.log("current_price is", price)
                
                var currentPriceUsdDiv = document.getElementById('buy-current-price-usd_' + index);
                
                //console.log("currentPriceUsdDiv", currentPriceUsdDiv)
                if (currentPriceUsdDiv) {
                    //console.log(currentPriceUsdDiv.dataset.value)
                    const currentPriceUsd = parseFloat(currentPriceUsdDiv.dataset.value)
                    //console.log("read price usd as", currentPriceUsd)
                    var total = units * currentPriceUsd
                } else {
                    var total = units * price
                }
                
                total = total.toFixed(2)
                //console.log("total is", total)
                //console.log("buy-order-value_" + index)
                
                content = "USD " + total
                //const cash_balance = "{{ portfolio.cash_balance }}"
                if (total > parseFloat(cash_balance)) {
                    triggerBuyNotAdequateCashMessage(index)
                }  else if (units > 0) {
                    triggerBuyValidMessage(index)
                } else {
                    deleteBuyMessages(index)
                }
            } else {
                if (str !== "") {
                    triggerBuyMultiplesMessage(index)
                    //console.log("has to be multiples of 0.01")
                } else {
                    deleteBuyMessages(index)
                }
            }
        } catch (error) {
            // Handle the error here if needed
            //console.error("An error occurred:", error);
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
            //console.log("str is", str)
            //console.log("current_units is", current_units)
            
            
            if (hasTwoOrFewerDecimalPoints(str)) {
                var units = parseFloat(str)
                //console.log("units is", units)
                //console.log("current_price is", price)
                
                var currentPriceUsdDiv = document.getElementById('sell-current-price-usd_' + index);
                
                //console.log("currentPriceUsdDiv", currentPriceUsdDiv)
                if (currentPriceUsdDiv) {
                    //console.log(currentPriceUsdDiv.dataset.value)
                    const currentPriceUsd = parseFloat(currentPriceUsdDiv.dataset.value)
                    //console.log("read price usd as", currentPriceUsd)
                    var total = units * currentPriceUsd
                } else {
                    var total = units * price
                }
                
                total = total.toFixed(2)
                //console.log("total is", total)
                //console.log("sell-order-value_" + index)
                
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
            //console.error("An error occurred:", error);
        }
        document.getElementById("sell-order-value_" + index).innerHTML = content
    });
}

function dropAssets() {
    var elements = document.getElementsByClassName("accordion-collapse");
    var elementsArray = Array.from(elements);
    
    // Remove class from each element
    elementsArray.forEach(function(element) {
        element.classList.add("show");
    });
}

function collapseAssets() {
    var elements = document.getElementsByClassName("accordion-collapse");
    var elementsArray = Array.from(elements);
    
    // Remove class from each element
    elementsArray.forEach(function(element) {
        element.classList.remove("show");
    });
}

function addMessage() {
    fetch(portfolio_id + '/get_advice', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(result => {
        const content = result['advice']
        const chatContainer = document.getElementById('chat-container');
        chatContainer.innerHTML = "";
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + "bot-message";
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
    })
}

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

function load_chart(ticker, index, width, chartObj) {
    //console.log("load_chart(ticker=", ticker,"index=", index,"width=", width,"chartObj=", chartObj)
    var chart = chartObj
    var myDiv = document.getElementById("asset_chart_two_" + index);
    myDiv.style.display = 'none';
    var myDiv = document.getElementById('asset_chart_spinner_' + index);
    myDiv.classList.remove('d-none');
    
    //console.log("updating candlestick chart", chart)
    
    fetch(portfolio_id + '/asset_data', {
        method: 'POST',
        body: JSON.stringify({
            ticker: ticker,
            width: width
        })
    })
    .then(response => response.json())
    .then(result => {
        //console.log("result load_chart(ticker=", ticker,"index=", index,"width=", width,"chartObj=", chart)
        
        /*         if ("ERROR" in result) {
            var myDiv = document.getElementById("asset_chart_error_" + index);
            myDiv.innerHTML = result.ERROR;
            myDiv.style.display = '';
        } else {
        } */

        // Print result
        var myDiv = document.getElementById("asset_chart_two_" + index);
        myDiv.style.display = '';
        
        var myDiv = document.getElementById('asset_chart_spinner_' + index);
        myDiv.classList.add('d-none');
        
        //console.log(result);
        var chartData = result.chart_data;
        
        //console.log("updating candlestick chart", chart)
        chart.data.datasets[0].data = chartData;
        chart.update();
    })
}

function initializeSearchAssetChart(callback) {
    // Create small chart
    var ctxSearchAssetChart = document.getElementById("search_asset_small_chart").getContext('2d');
    var existingChart = Chart.getChart(ctxSearchAssetChart)
    if (existingChart) {
        // Destroy the existing chart
        existingChart.destroy();
    }
    ctxSearchAssetChart.canvas.width = '200px';
    ctxSearchAssetChart.canvas.height = '50px';
    var searchAssetChart = new Chart(ctxSearchAssetChart, _.cloneDeep(smallAssetChartConfig));
    callback(searchAssetChart)
}

function initializeSearchAssetPriceChart(callback) {
    
    // Create price chart
    var ctxSearchAssetPriceChart = document.getElementById("search_asset_price_chart").getContext('2d');
    var existingChart = Chart.getChart(ctxSearchAssetPriceChart)
    if (existingChart) {
        // Destroy the existing chart
        existingChart.destroy();
    }
    ctxSearchAssetPriceChart.canvas.width = '898px';
    ctxSearchAssetPriceChart.canvas.height = '150px';
    var searchAssetPriceChart = new Chart(ctxSearchAssetPriceChart, _.cloneDeep(assetPriceChartConfig));
    callback(searchAssetPriceChart)
}

function initializeCandlestickSearchAssetChart(callback) {
    // Create candlestick chart
    //console.log("making candlestick chart for search asset");
    var myDiv = document.getElementById("asset_chart_two_" + "search_asset").getContext('2d');
    var existingChart = Chart.getChart(myDiv)
    if (existingChart) {
        // Destroy the existing chart
        existingChart.destroy();
    }
    //console.log("myDiv", myDiv);
    var candlestickSearchAssetChart = new Chart(myDiv, _.cloneDeep(assetCandlestickChartConfig));
    callback(candlestickSearchAssetChart)
}

function initializeSearchBetaChart(callback) {
    // Create price chart
    var ctxSearchBetaChart = document.getElementById("asset_chart_beta_search").getContext('2d');
    var existingChart = Chart.getChart(ctxSearchBetaChart)
    if (existingChart) {
        // Destroy the existing chart
        existingChart.destroy();
    }
    ctxSearchBetaChart.canvas.width = '898px';
    ctxSearchBetaChart.canvas.height = '150px';
    var searchBetaChart = new Chart(ctxSearchBetaChart, _.cloneDeep(assetBetaChartConfig));
    callback(searchBetaChart)
}

function load_search_asset_charts() {

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
}

/*
*   Searches for asset and displays information based on response
*/
function search_asset(searchAssetChart, searchAssetPriceChart, candlestickSearchAssetChart) {
    //console.log("search_ticker:", ticker)
    console.log("making a call to search asset")

    var ticker = document.getElementById("search_ticker").value;
    
    // Don't search for empty search queries
    if (ticker.trim() === "") {
        console.log("ticker is empty")
        return
    }

    var errorDiv = document.getElementById("search_asset_error");
    var assetDataDiv = document.getElementById("search_asset_data");
    var spinnerDiv = document.getElementById('search_asset_spinner');
    
    assetDataDiv.style.display = 'none';
    errorDiv.classList.add('d-none');
    spinnerDiv.classList.remove('d-none');
    
    fetch(portfolio_id + '/search_asset', {
        method: 'POST',
        body: JSON.stringify({
            ticker: ticker
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        var errorDiv = document.getElementById("search_asset_error");
        var spinnerDiv = document.getElementById('search_asset_spinner');

        if ("ERROR" in result) {
            errorDiv.innerHTML = result.ERROR;
            errorDiv.classList.remove('d-none');
            spinnerDiv.classList.add('d-none');
            return
        } else {
            errorDiv.classList.add('d-none');
        }

        // Update info
        document.getElementById("search_asset_ticker").innerHTML = result.ticker;
        document.getElementById("search_asset_long_name").innerHTML = result.long_name;

        // Check if the condition is fulfilled
        if (result.currency !== "USD") {
            // If condition is fulfilled, construct the HTML string with the div
            var htmlContent = '<small style="font-size: 9px; margin-right:2px;"> ' + result.currency + ' </small>';
        } else {
            // If condition is not fulfilled, construct the HTML string without the div
            var htmlContent = '';
        }

        // Add the HTML content to the element with id "search_asset_price"
        document.getElementById("search_asset_price").innerHTML = htmlContent + result.current_price;

        //document.getElementById("search_asset_price").innerHTML = result.current_price;
        var change_button = document.getElementById("search_asset_price_change")
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
        
        document.getElementById("search_asset_currency").innerHTML = result.currency;
        document.getElementById("search_asset_country").innerHTML = result.country;
        document.getElementById("search_asset_quote_type").innerHTML = result.quote_type;
        document.getElementById("search_asset_exchange").innerHTML = result.exchange;
        document.getElementById("search_asset_summary").innerHTML = result.long_business_summary;
        
        if (result.current_price_change_status === "NEGATIVE") {
            var price_chart_border_color = CHART_COLOURS.RED_BORDER;
            var price_chart_background_color = CHART_COLOURS.RED_BACKGROUND;
        } else {
            var price_chart_border_color = CHART_COLOURS.GREEN_BORDER;
            var price_chart_background_color = CHART_COLOURS.GREEN_BACKGROUND;
        }

        console.log("price_chart_border_color", price_chart_border_color);
        console.log("price_chart_background_color", price_chart_background_color);
        
        var price_chart_date = JSON.parse(result.price_chart).date;
        var price_chart_price = JSON.parse(result.price_chart).price;
        
        var chartData = result.chart_data;
        
        initializeSearchAssetChart(function (searchAssetChart) {
            console.log("searchAssetChart.data", searchAssetChart.data);
            // Now you can safely update the chart
            searchAssetChart.data.labels = price_chart_date
            searchAssetChart["data"]["datasets"][0] = {
                data: price_chart_price,
                fill: true,
                backgroundColor: price_chart_background_color,
                borderColor: price_chart_border_color,
                borderWidth: 2.5,
                pointRadius: 0,
                pointHoverRadius: 0,
            }
            searchAssetChart.data.datasets[0].backgroundColor = (context) => {
                const { ctx, data, chartArea: {top, bottom} } = context.chart;
                //console.log("top", top, ": bottom", bottom)
                const gradientBg = ctx.createLinearGradient(0, top, 0, top + 47);
                gradientBg.addColorStop(1, 'rgba(255, 255, 255, 0.3)')
                gradientBg.addColorStop(0, price_chart_background_color)
                return gradientBg;
            }
            
            searchAssetChart.update();
        });
        
        initializeSearchAssetPriceChart(function (searchAssetPriceChart) {
            searchAssetPriceChart.data.labels = price_chart_date
            searchAssetPriceChart["data"]["datasets"][0] = {
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
            searchAssetPriceChart.data.datasets[0].backgroundColor = (context) => {
                const { ctx, data, chartArea: {top, bottom} } = context.chart;
                //console.log("top", top, ": bottom", bottom)
                const gradientBg = ctx.createLinearGradient(0, top, 0, top + 160);
                gradientBg.addColorStop(1, 'rgba(255, 255, 255, 0.3)')
                gradientBg.addColorStop(0, price_chart_background_color)
                return gradientBg;
            }
            searchAssetPriceChart.update();
        });
        
        initializeCandlestickSearchAssetChart(function (candlestickSearchAssetChart) {
            load_chart(result.ticker, "search_asset",'threeM', candlestickSearchAssetChart);
        });

        const beta_chart = result.beta_chart
        console.log("beta_chart", beta_chart)

        var line_plot_data = beta_chart[0].line_plot_data;
        var scatter_plot_data = beta_chart[0].scatter_plot_data;
        var beta = beta_chart[0].beta;
        var benchmark = beta_chart[0].benchmark;

        initializeSearchBetaChart(function (betaSearchAssetChart) {
            betaSearchAssetChart["data"]["datasets"] = [{
                    type: 'scatter',
                    label: 'Scatter Plot',
                    data: scatter_plot_data,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                },
                {
                    type: 'line',
                    label: 'Linear Plot',
                    data: line_plot_data,
                    borderColor: 'rgba(75, 192, 192, 0.5)',
                    borderWidth: 3,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                }]
            betaSearchAssetChart.update()
        });

        document.getElementById("search_asset_beta_value").innerHTML = "Beta = " + beta;
        document.getElementById("search_asset_beta_benchmark").innerHTML = "Benchmark = " + benchmark;
        
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

function articleCard(article, i) {

    var container = document.createElement('a');
    
    // TODO: Figure out way to remove all weird images. Like empty ones, white.
    if (article.banner_image === null) {
        article.banner_image = alt_image_url
    }
    
    var inner_html = `
    <div class="row g-0">
    <div class="image_container">
    <img src="${article.banner_image}" class="img-fluid rounded-start d-block" alt="Descriptive text about your primary image"
    onerror="this.onerror=null;">
    </div>
    <div class="news-content">
    <div class="card-body" style="padding-top: 10px; padding-bottom: 0px;">
    <div style="height: 165px;">
    <h6 style="margin-bottom: 0px;">${article.source}</h6>
                            <h5 class="card-title" style="font-weight: heavy; margin-bottom: 2px;">${ article.title }</h5>
                            <p class="card-text" style="font-size: 12px;">${ article.summary }</p>
                        </div>
                        <p class="card-text"><small class="text-body-secondary" style="font-size: 12px;">${ article.time_published }</small></p>
                    </div>
                </div>
            </div>
    `;
    
    container.id= `article_${i}`;
    container.classList.add("card", "mb-3", "carousel-item", "news_card");
    if (i === 0) {
        container.classList.add("active");
    }
    container.innerHTML = inner_html;

    //console.log("container", container)
    container.addEventListener('click', function() {
        openInNewTab(article.url)
    })
    return container;
}

function addNews() {
    fetch(portfolio_id + '/get_news', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(result => {
        const news = result['news']
        if (news !== null) {
            document.getElementById('news-Div').style = "block"
            var newsContainer = document.getElementById('news-container');

            news.feed.forEach((article, index) => {
                //console.log(`Generating news item for ${index}: ${article}`);
                newsContainer.appendChild(articleCard(article, index));
            });
        }
    })
}

function openInNewTab(url) {
    var win = window.open(url, '_blank');
    win.focus();
}

// Add event listeners to buttons search bars etc.
document.addEventListener('DOMContentLoaded', function () {
    
    // Assuming you are using Bootstrap's data-bs-target attribute to identify the accordion element
    document.getElementById('showAllButton').addEventListener('click', function() {
        //console.log("showAllButton clicked...")
        var accordionButtons = document.querySelectorAll('.accordion-button.collapsed');
        //console.log("collapsed buttons", accordionButtons)
        accordionButtons.forEach(button => button.click())
    });
    
    document.getElementById('collapseAllButton').addEventListener('click', function() {
        //console.log("collapseAllButton clicked...")
        
        var accordionButtons = document.querySelectorAll('.accordion-button:not(.collapsed)');
        //console.log("non collapsed buttons", accordionButtons)
        
        accordionButtons.forEach(button => button.click())
    });
    
    document.getElementById("buy-num-units_search_asset").addEventListener("keyup", function(event) {
        var content = "USD 0.00"
        
        try {
            var index = "search_asset"
            var price = parseFloat(event.target.dataset.price)
            var str = event.target.value
            //console.log("str is", str)
            
            if (hasTwoOrFewerDecimalPoints(str)) {
                var units = parseFloat(str)
                //console.log("units is", units)
                //console.log("current_price is", price)
                
                var total = units * price
                total = total.toFixed(2)
                //console.log("total is", total)
                //console.log("buy-order-value_" + index)
                
                content = "USD " + total
                if (total > parseFloat(cash_balance)) {
                    triggerBuyNotAdequateCashMessage(index)
                }  else if (units > 0) {
                    triggerBuyValidMessage(index)
                } else {
                    deleteBuyMessages(index)
                }
            } else {
                if (str !== "") {
                    triggerBuyMultiplesMessage(index)
                    //console.log("has to be multiples of 0.01")
                } else {
                    deleteBuyMessages(index)
                }
            }
        } catch (error) {
            // Handle the error here if needed
            //console.error("An error occurred:", error);
        }
        document.getElementById("buy-order-value_search_asset").innerHTML = content
    })
});

const CHART_COLOURS = {
    RED_BORDER: 'rgba(255, 75, 66, 1)',
    RED_BACKGROUND: 'rgba(255, 75, 66, 0.15)',
    RED_BACKGROUND_GRAD: 'rgba(255, 75, 66, 0.4)',
    RED_BACKGROUND_GRAD_LOW: 'rgba(255, 75, 66, 0.1)',
    GREEN_BORDER: 'rgba(100, 220, 150, 1)',
    GREEN_BACKGROUND: 'rgba(100, 220, 150, 0.15)',
    GREEN_BACKGROUND_GRAD: 'rgba(100, 220, 150, 0.4)',
    GREEN_BACKGROUND_GRAD_LOW: 'rgba(100, 220, 150, 0.1)',
    TOOLTIP_COLOR: 'rgba(13, 110, 253, 1)',
};

const assetMixColours = ['rgba(100, 220, 150, 1)', 'rgba(255, 165, 0, 1)', 'rgba(0, 123, 255, 1)', 'rgba(76, 169, 255, 143)', 'rgba(56, 122, 122, 1)', 'rgba(122, 32, 190, 1)'];

/* const delayBetweenPoints = 10;
const previousY = (ctx) => ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(100) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;
const animation = {
  x: {
    type: 'number',
    easing: 'linear',
    duration: delayBetweenPoints,
    from: NaN, // the point is initially skipped
    delay(ctx) {
      if (ctx.type !== 'data' || ctx.xStarted) {
        return 0;
      }
      ctx.xStarted = true;
      return ctx.index * delayBetweenPoints;
    }
  },
  y: {
    type: 'number',
    easing: 'linear',
    duration: delayBetweenPoints,
    from: previousY,
    delay(ctx) {
      if (ctx.type !== 'data' || ctx.yStarted) {
        return 0;
      }
      ctx.yStarted = true;
      return ctx.index * delayBetweenPoints;
    }
  }
}; */

var portfolioValueChartConfig = {
    type: 'line',
    data: {
        labels: price_data["date"],
        datasets: [{
            data: price_data["value"],
            backgroundColor: null,
            borderColor: null,
            borderWidth: 3,
            pointRadius: 10,
            pointBorderColor: 'rgba(100, 220, 150, 0)',
            pointBackgroundColor: 'rgba(100, 220, 150, 0)',
            pointHoverRadius: 10,
            pointHoverBackgroundColor: null,
            pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
            pointHoverBorderWidth: 3,
            fill: true,
        }]
    },
    options: {
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
          },
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
                    display: false,
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
};

var assetMixChartConfig = {
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
        
        plugins: {
            animation: false,
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
              },
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
};

const smallAssetChartConfig = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            data: null,
            fill: true,
            backgroundColor: null,
            borderColor: null,
            borderWidth: 2.5,
            pointRadius: 0,
            pointHoverRadius: 0,
        }]              
    },
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
            animation: false,
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
};

const assetPriceChartConfig = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            data: null,
            fill: true,
            borderWidth: 3,
            pointRadius: 10,
            pointBorderColor: 'rgba(100, 220, 150, 0)',
            pointBackgroundColor: 'rgba(100, 220, 150, 0)',
            pointHoverRadius: 10,
            pointHoverBackgroundColor: null,
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
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
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
                bodyAlign: 'right'                      
            },
        }
    }
};

const assetCandlestickChartConfig = {
    type: 'candlestick',
    data: {
        datasets: [{
            label: [],
            data: [],
            pointBackgroundColor: 'white',
            pointBorderColor: 'white',
            pointBorderWidth: 0,
            // Custom colors for bullish and bearish candlesticks
            backgroundColor: {
                up: '#111111', // color for rising prices
                down: CHART_COLOURS.RED_BACKGROUND  // color for falling prices
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
};

const assetBetaChartConfig = {
    data: {
        datasets: []
    },
    options: {
        scales: {
            x: {
                border: {
                    display: true
                },
                title: {
                    display: true,
                    text: 'Benchmark: Daily % change',
                    font: {
                        style: 'bold',
                    },
                    /*color: '#191',
                     font: {
                      family: 'Times',
                      size: 20,
                      style: 'normal',
                      lineHeight: 1.2
                    }, */
                    padding: {top: 10, left: 0, right: 0, bottom: 0}
                  },
                beginAtZero: false,
                ticks: {
                    maxTicksLimit: 8, // Set the maximum number of x-axis labels
                    maxRotation: 0,   // Set the maximum label rotation angle
                    minRotation: 0,
                    align: 'start',

                    font: {
                        size: 14,
                        weight: 'bold'
                    },  
                },
                grid: {
                    color: 'rgba(1, 255, 255, 0)'
                },
            },
            y: {
                border: {
                    display: true
                },
                title: {
                    display: true,
                    text: 'Asset: Daily % change',
                    font: {
                        style: 'bold',
                    },
                    /*color: '#191',
                      family: 'Times',
                      size: 20,
                      lineHeight: 1.2
                    }, */
                    padding: {top: 0, left: 0, right: 0, bottom: 10}
                  },
                beginAtZero: false,
                position: 'right',
                ticks: {
                    // You can add additional y-axis tick options here if needed
                    maxTicksLimit: 8, // Set the maximum number of x-axis labels
                    includeBounds: true,
                    crossAlign: 'near',
                    font: {
                        size: 14,
                        weight: 'bold'
                    },  
                },
                grid: {
                    color: 'rgba(1, 255, 255, 0)'
                },
            },
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
                bodyAlign: 'right'                      
            },
        }
    }
};