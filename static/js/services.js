function addFeature(uuid, name, distribution, defaults, params) {

    feature = {}
    feature[name] = {};
    feature[name]['distribution'] = distribution;
    feature[name]['default'] = defaults;
    feature[name]['params'] = params;

    $.ajax({
        contentType: 'application/json',
        data: JSON.stringify(feature),
        dataType: 'json',

        success: function(data){
            console.log("feature added");
        },
        error: function(){
            console.log("error feature addition");
        },
        processData: false,
        type: 'POST',
        url: '/api/feature/' + uuid
    });

}

function removeFeature(uuid, name) {

    $.ajax({
        contentType: 'application/json',
        data: JSON.stringify({'feature_name': name}),
        dataType: 'json',

        success: function(data){
            console.log("feature removed");
        },
        error: function(){
            console.log("error feature removal");
        },
        processData: false,
        type: 'DELETE',
        url: '/api/feature/' + uuid
    });

}
