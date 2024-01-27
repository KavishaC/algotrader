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
    } else {
        borderColor = CHART_COLOURS.GREEN_BORDER;
        backgroundColor = CHART_COLOURS.GREEN_BACKGROUND;
    }
    
    var portfolioValueChart = new Chart(ctx, portfolioValueChartConfig);
    
    portfolioValueChart.data.datasets[0].backgroundColor = backgroundColor;
    portfolioValueChart.data.datasets[0].borderColor = borderColor;
    portfolioValueChart.data.datasets[0].pointHoverBackgroundColor = borderColor
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
        price_chart_border_color = CHART_COLOURS.RED_BORDER;
        price_chart_background_color = CHART_COLOURS.RED_BACKGROUND;
    } else {
        price_chart_border_color = CHART_COLOURS.GREEN_BORDER;
        price_chart_background_color = CHART_COLOURS.GREEN_BACKGROUND;
    }
    
    var price_chart_date = JSON.parse(asset.price_chart).date
    var price_chart_price = JSON.parse(asset.price_chart).price
    //console.log("last price for", asset.index, "is", price_chart_price)
    
    var smallAssetChart = new Chart(ctxAssetChart, _.cloneDeep(smallAssetChartConfig));
    smallAssetChart.data.labels = price_chart_date;
    smallAssetChart.data.datasets[0].data = price_chart_price;
    smallAssetChart.data.datasets[0].backgroundColor = price_chart_background_color;
    smallAssetChart.data.datasets[0].borderColor = price_chart_border_color;
    smallAssetChart.update()
}

function createAssetPriceChart(asset) {
    //console.log("creating asset chart for", asset)
    
    var ctxPriceChart = document.getElementById("price_chart_" + asset.index).getContext('2d');
    ctxPriceChart.canvas.width = '898px';
    ctxPriceChart.canvas.height = '150px';
    
    var price_chart_border_color;
    var price_chart_background_color;
    
    if (asset.current_price_change_status === "NEGATIVE") {
        price_chart_border_color = CHART_COLOURS.RED_BORDER;
        price_chart_background_color = CHART_COLOURS.RED_BACKGROUND;
    } else {
        price_chart_border_color = CHART_COLOURS.GREEN_BORDER;
        price_chart_background_color = CHART_COLOURS.GREEN_BACKGROUND;
    }
    
    var price_chart_date = JSON.parse(asset.price_chart).date
    var price_chart_price = JSON.parse(asset.price_chart).price
    //console.log("last price for", asset.index, "is", price_chart_price)
    
    var assetPriceChart = new Chart(ctxPriceChart, _.cloneDeep(assetPriceChartConfig));
    assetPriceChart.data.labels = price_chart_date;
    assetPriceChart.data.datasets[0].data = price_chart_price;
    assetPriceChart.data.datasets[0].backgroundColor = price_chart_background_color;
    assetPriceChart.data.datasets[0].borderColor = price_chart_border_color;
    assetPriceChart.data.datasets[0].pointHoverBackgroundColor = price_chart_border_color;
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

function load_search_asset_charts() {
    
    // Create small chart
    var ctxSearchAssetChart = document.getElementById("search_asset_small_chart").getContext('2d');
    ctxSearchAssetChart.canvas.width = '200px';
    ctxSearchAssetChart.canvas.height = '50px';
    
    var searchAssetChart = new Chart(ctxSearchAssetChart, smallAssetChartConfig);
    
    // Create price chart
    var ctxSearchAssetPriceChart = document.getElementById("search_asset_price_chart").getContext('2d');
    ctxSearchAssetPriceChart.canvas.width = '898px';
    ctxSearchAssetPriceChart.canvas.height = '150px';
    
    var searchAssetPriceChart = new Chart(ctxSearchAssetPriceChart, assetPriceChartConfig);
    
    // Create candlestick chart
    //console.log("making candlestick chart for search asset");
    var myDiv = document.getElementById("asset_chart_two_" + "search_asset").getContext('2d');
    //console.log("myDiv", myDiv);
    
    var candlestickSearchAssetChart = new Chart(myDiv, assetCandlestickChartConfig);
    
    
    var searchButton = document.getElementById("search_trigger");
    
    // Add an event listener to the button and attach the search_asset function
    searchButton.addEventListener("click", search_asset);
    
    var searchInput = document.getElementById("search_ticker");
    // Add an event listener for the "keyup" event
    searchInput.addEventListener("keyup", function(event) {
        // Check if the "Enter" key (key code 13) was pressed
        if (event.key === "Enter") {
            // Call the search_asset function when "Enter" is pressed
            search_asset(searchAssetChart, searchAssetPriceChart, candlestickSearchAssetChart);
        }
    });
}

/*
*   Searches for asset and displays information based on response
*/
function search_asset(searchAssetChart, searchAssetPriceChart, candlestickSearchAssetChart) {
    //console.log("search_ticker:", ticker)

    var ticker = document.getElementById("search_ticker").value;
    
    // Don't search for empty search queries
    if (ticker.trim() === "") {
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
        //console.log(result)
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
        document.getElementById("search_asset_price").innerHTML = result.current_price;
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
        
        var price_chart_date = JSON.parse(result.price_chart).date;
        var price_chart_price = JSON.parse(result.price_chart).price;
        
        //console.log(price_chart_date, price_chart_price);
        
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
    GREEN_BORDER: 'rgba(100, 220, 150, 1)',
    GREEN_BACKGROUND: 'rgba(100, 220, 150, 0.15)',
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
            fill: true,
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
        labels: null,
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
        labels: null,
        datasets: [{
            data: null,
            fill: true,
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
                bodyAlign: 'right'                      
            },
        }
    }
};

const assetCandlestickChartConfig = {
    type: 'candlestick',
    data: {
        datasets: [{
            label: null,
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
