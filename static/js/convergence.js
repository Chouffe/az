function toggleGraphDataToDisplay() {

    var toggleValue = false;
    for ( var varName in graphDataToDisplay ) {
        if ( !graphDataToDisplay[varName] ) {
            toggleValue = true;
            break;
        }
    }

    for ( var varName in graphDataToDisplay ) {
        graphDataToDisplay[varName] = toggleValue;
    }
}

function assignCheckboxValues() {

    var features = getFeatures(graphsData);

    $("#convergence-checkboxes label").remove();
    var labels = d3.select("#convergence-checkboxes")
    .selectAll("label")
    .data(features)
    .enter().append("label")
    .attr("class", "inline-checkbox")
    .text(function (d) { return d; })

    labels.append("input")
    .attr("type", "checkbox")
    .attr("checked", function (d) { if ( !graphDataToDisplay[d]) { return null; } else { return "checked"; }})
    .on("change", function (d) {
        // Toggle
        if (graphDataToDisplay[d]) {
            graphDataToDisplay[d] = false;
        }
        else {
            graphDataToDisplay[d] = true;
        }
        cleanUpGraph();
        plotGraphsToDisplay(); })

}


function loadGraphData(uuid) {

    $.get( "/api/graph/results/" + uuid, function( dataString ) {
        var data = $.parseJSON(dataString);
        graphsData = data;

        // Initializes graphs to display
        if ( graphDataToDisplay == undefined ) {
            graphDataToDisplay = {}
            for (var varName in data) {
                graphDataToDisplay[varName] = true;
            }
        }

        assignCheckboxValues();
        plotGraphsToDisplay();
    });
}

function loadABGraphData(uuid) {

    $.get( "/api/ab/graph/results/" + uuid, function( dataString ) {
        var data = $.parseJSON(dataString);
        abGraphsData = data;
        console.log(data);
        plotABGraphsToDisplay();
    });

}


function plotGraphsToDisplay() {

    cleanUpGraph();
    var features = getFeatures(graphsData);

    for(var i in features) {

        varName = features[i];
        if (graphDataToDisplay[varName]) {
            ydata = graphsData[varName];
            xdata = range(ydata.length);
            drawChart(xdata, ydata, "draw #", varName, "#charts");
        }
    }

}

function plotABGraphsToDisplay() {

    console.log('test');
    cleanUpABGraph();
    var features = getFeatures(abGraphsData);
    console.log(features);

    for(var i in features) {

        varName = features[i];
        if (graphDataToDisplay[varName]) {
            ydata = abGraphsData[varName];
            xdata = range(ydata.length);
            drawChart(xdata, ydata, "draw #", varName, "#ab-charts");
        }
    }

}

function cleanUpGraph() {
    $("#charts .chart").remove();
}

function cleanUpABGraph() {
    $("#ab-charts .chart").remove();
}


