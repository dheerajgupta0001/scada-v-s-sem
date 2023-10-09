function loadPlotData() {
    dataKeysGlob = Object.keys(dfData_gGlob);
    for (let maesIterGlob = 0; maesIterGlob < dfData_gGlob.length; maesIterGlob++) {
        var dfData_g = dfData_gGlob[maesIterGlob]
        console.log(dfData_g)
        var dateKeyName = 'TIME_STAMP';
        var TIME_STAMP = dfData_g[dateKeyName];
        // create traces array
        traces = [];
        dataKeys = Object.keys(dfData_g);
        for (let measIter = 0; measIter < dataKeys.length; measIter++) {
            var meas = dataKeys[measIter];
            if (meas == dateKeyName) {
                continue;
            }
            var trace = {
                x: TIME_STAMP,
                y: dfData_g[meas],
                mode: 'lines',
                name: meas
            };
            traces.push(trace);
        }
        var layout = {
            title:{
                text: linesDisplayList[maesIterGlob],
                font: {
                    family: "Times New Roman",
                    size: 35,
                    color: "blue"
                }
            },
            showlegend: true,
            legend: { "orientation": "v" },
            paper_bgcolor: "#e5e5e5"
        };
        Plotly.newPlot(linesName[maesIterGlob], traces, layout);
    }
}