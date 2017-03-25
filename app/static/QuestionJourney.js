var QuestionJourney = (function () {
    'use strict';

    function init (opts) {
        var travel = new Travel(opts);
        travel.registerEvents();
        travel.initDatetimePicker();
    }



    function Travel (opts) {
       this.timeFrameSpecified = false;
       this.timeFrame = null;
       this.step = 1;
       this.$timeNextButton = opts.$timeNextButton || null;
       this.$from = opts.$from;
       this.$to = opts.$to;
       this.$durationTiles = opts.$durationTiles;
       this.$regionMap = opts.$regionMap;
       this.$step1 = opts.$step1;
       this.$step2 = opts.$step2;
       this.$step3 = opts.$step3;
    }

    var nextStep2 = function (self) {
        self.$step1.hide();
        self.$step2.show();
    };

    var nextStep3 = function (self) {
        self.$step2.hide();
        self.$step3.show();
    };

    var nextStep4 = function (self) {
        window.location.href = "/results"
    };


    Travel.prototype.registerEvents = function () {
        var self = this;
        this.$timeNextButton.on('click', function () {
            nextStep2(self);
        });
        this.$durationTiles.on('click', function () {
            nextStep3(self);
        });
        this.$regionMap.on('click', function () {
            nextStep4(self);
        });
    };

    Travel.prototype.initDatetimePicker = function () {
        this.$from.datetimepicker({format: "L"});
        this.$to.datetimepicker({format: "L"});
    };

    return {
        init: init
    }
})();