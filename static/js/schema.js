function loadSchema(uuid) {

    $.get( "/api/schema/" + uuid, function( dataString ) {
        schema = $.parseJSON(dataString);

        features = getFeatures(schema['features']);

        $("#schema-table tbody tr").remove();

        d3.select("#schema-table tbody")
        .selectAll('tr')
        .data(features)
        .enter().append('tr')
        .selectAll('td')
        .data(function(d) {
            return [d, schema['features'][d]['default'], schema['features'][d]['distribution'], JSON.stringify(schema['features'][d]['params']), "<a class='btn btn-danger' onclick='return deleteFeature(\""+ d + "\");'>x</a>"] })
            .enter().append('td')
            .html(function (d) { return d });

    });
}

