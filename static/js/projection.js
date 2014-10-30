function loadObjectiveFunctionData(uuid) {

    $.get( "/api/graph/obj/" + uuid, function( dataString ) {

        var data = $.parseJSON(dataString);

        // Debugging
        objectiveFunctionData = data;

        $("#objective-function .chart").remove();

        var features = [];
        for (var varName in data) {
            features.push(varName);
        }

        features.sort();

        d3.select("#objective-function-select-parameter")
        .selectAll('option')
        .data(features)
        .enter().append('option')
        .attr('value', function (d) { return d; })
        .text(function (d) { return d; });

        if (features.length > 0) {

            feature = features[0]
            xdata = data[feature].x;
            ydata = data[feature].y;

            drawScatterChart(xdata, ydata, feature, 'f(' + feature +')', "#objective-function");

        }

    });

}

