function getFeatures(data) {
    var features = [];
    for (var varName in data) {
        features.push(varName);
    }

    features.sort();
    return features;
}

