// Copyright (c) 2024, DarkMatter-999 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Water Meter', {
    meter_latitude: function(frm) {
        update_marker(frm);
    },
    meter_longitude: function(frm) {
        update_marker(frm);
    }
});

function update_marker(frm) {
    if (frm.doc.meter_latitude && frm.doc.meter_longitude) {
        var latitude = parseFloat(frm.doc.meter_latitude);
        var longitude = parseFloat(frm.doc.meter_longitude);
        
        var geojson = {
            type: "FeatureCollection",
            features: [{
                type: "Feature",
                properties: {},
                geometry: {
                    type: "Point",
                    coordinates: [longitude, latitude]
                }
            }]
        };
        
        frm.set_value('meter_coordinates', JSON.stringify(geojson));
    }
}
