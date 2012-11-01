Noodle.Alert = (function() {

    /* public functions */
    var renderAlert = function(alert) {
        var $box = $(Noodle.Dom.Alert.ALERT);
        $box.empty();
        $box.append(alert);
    };

    return {
        render: renderAlert
    }
})();
