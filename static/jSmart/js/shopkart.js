// Próximo passo: Ao carregar a página, alterar o status dos botões de acordo com o valor
// do atributo data-kart-item-status.

/*!
 * Shopkart.js v0.3.3
 * Copyright 2018
 * Original author: Eduardo Vinicius Micami
 * Email eduvnsm@gmail.com
 * Version: 1.0.0
 * Licensed MIT
 */

// the semi-colon before the function invocation is a safety net against concatenated
// scripts and/or other plugins that are not closed properly.
;+function ($, window, undefined) {

    /**
     * Detects whether localStorage is both supported and available.
     * https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API#Testing_for_availability
     * @param  {string} type
     * @return {boolean}
     */
    function storageAvailable(type) {
        try {
            var storage = window[type],
                x = '__storage_test__';
            storage.setItem(x, x);
            storage.removeItem(x);
            return true;
        }
        catch(e) {
            return e instanceof DOMException && (
                // everything except Firefox
                e.code === 22 ||
                // Firefox
                e.code === 1014 ||
                // test name field too, because code might not be present
                // everything except Firefox
                e.name === 'QuotaExceededError' ||
                // Firefox
                e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
                // acknowledge QuotaExceededError only if there's something already stored
                storage.length !== 0;
        }
    }

    if (!storageAvailable('localStorage')) {
        window.alert("Atention!\nThis browser does not support Storage API.\nSome functionality might not work properly. :(");
        throw new Error("Atention!\nThis browser does not support Storage API.\nSome functionality might not work properly. :(");
    }

    $.shopkart = function (options) {
        "use strict"; // strict method

        /**
         * Default configuration options.
         *
         * @type {Object}
         */
        var defaults = {
            kartItemButtonText: {
                add: "Add to Cart",
                remove: "Remove"
            },
            kartItemButtonStatus: {
                add: "add-item",
                remove: "remove-item"
            },
            /**
             * Allow to format the total items text.
             * @return {string} The total of items
             */
            formatTotalItem: function () {},
            /**
             * Allow to format the total price.
             * @return {string} The total price formatted.
             */
            formatTotalPrice: function () {},
            /**
             * Allow to customize the add button
             * @param {Object} The add button
             * @return {void}
             */
            styleButtonAddItem: function () {},
            /**
             * Allow to customize the remove button
             * @param {Object} $button The remove button
             * @return {void}
             */
            styleButtonRemoveItem: function () {},
        };

        /**
         * Extend the default options with those provided.
         * Note that the first argument to extend is an empty object
         * – this is to keep from overriding our "defaults" object.
         *
         * @type {Object}
         */
        var opts = $.extend({}, defaults, options);

        // Checks if the add button data value is defined
        if (!opts.kartItemButtonStatus.hasOwnProperty("add")) {
            alert("The kartItemButtonStatus option requires the add property value!");
            console.log("The kartItemButtonStatus option requires the add property value!");
        }
        // Checks if the remove button data value is defined
        if (!opts.kartItemButtonStatus.hasOwnProperty("remove")) {
            alert("The kartItemButtonStatus option requires the remove property value!");
            console.log("The kartItemButtonStatus option requires the remove property value!");
        }

        /*____________________ DOM Cache ____________________*/
        /**
         * The cart display object.
         * @type {Object}
         */
        var $kartDisplay = $('[data-kart="display"]');
        /**
         * The cart display of total item object
         * @type {Object}
         */
        var $kartDisplayTotalItem = $kartDisplay.find("[data-kart-total-item]");
        /**
         * The cart display of total price object
         * @type {Object}
         */
        var $kartDisplayTotalPrice = $kartDisplay.find("[data-kart-total-price]");
        /**
         * The cart add/remove button elements.
         * @type {Object}
         */
        var $kartButtons = $('[data-kart=item-button]');
        /**
         * The current add/remove clicked button element.
         * @type {Object}
         */
        var $kartCurrentButton = null;

        /*____________________ Initialize local storage values____________________*/
        /**
         * An object that keeps track of the cart sessions
         * @type {Kart}
         */
        localStorage.removeItem('shopkart'); // This is temporary until basic functionalities are done
        var oKart = localStorage.getItem('shopkart') || new Kart();

        /*____________________ Add event listeners ____________________*/
        $kartButtons.on("click", function () {
            $kartCurrentButton = $(this);

            var btnStatus = $kartCurrentButton.data("kart-item-status");
            var oItem = $kartCurrentButton.data("kart-item");

            toggleButtonItemStatus(oItem, btnStatus);

            console.log(oItem);
            var price = oItem.price ? oItem.price : $kartCurrentButton.data("kart-item-price");
            updateKartDisplay(btnStatus, price);
        });

        /**
         * Toggles the status of the current clicked button element.
         * @param  {Object} oItem The object from 'kart-item' attribute
         * @param  {string} status The status of the current clicked button element
         * @return {void}
         */
        function toggleButtonItemStatus(oItem, status) {
            // do add item stuffs
            if (status === opts.kartItemButtonStatus.add) {
                $kartCurrentButton
                    .data("kart-item-status", opts.kartItemButtonStatus.remove)
                    .html(opts.kartItemButtonText.remove);
                oKart.addItem(oItem);
                if (opts.styleButtonRemoveItem.length > 0 && typeof opts.styleButtonRemoveItem === "function") {
                    // apply the remove button custom style
                    opts.styleButtonRemoveItem($kartCurrentButton);
                }
            }
            // do remove item stuffs
            if (status === opts.kartItemButtonStatus.remove) {
                $kartCurrentButton
                    .data("kart-item-status", opts.kartItemButtonStatus.add)
                    .html(opts.kartItemButtonText.add);
                oKart.removeItem("id", oItem.id);
                if (opts.styleButtonAddItem.length > 0 && typeof opts.styleButtonAddItem === "function") {
                    // apply the add button custom style
                    opts.styleButtonAddItem($kartCurrentButton);
                }
            }

            var _totalItems = oKart.getTotalItem();
            // display the total of items in the cart
            if (opts.formatTotalItem.length > 0 && typeof opts.formatTotalItem === "function") {
                $kartDisplayTotalItem.html(opts.formatTotalItem(_totalItems));
            } else {
                $kartDisplayTotalItem.html(_totalItems);
            }
        }

        /**
         * Updates the cart total price and cart total item.
         * @param  {String} status The status of the user action (add|remove)
         * @param  {double} price  The price of the item
         * @return {void}
         */
        function updateKartDisplay(status, price) {
            if (status === opts.kartItemButtonStatus.add) {
                oKart.addTotalPrice(price);
            }
            if (status === opts.kartItemButtonStatus.remove) {
                oKart.subtractTotalPrice(price);
            }

            var _totalPrice = oKart.getTotalPrice();
            var _totalItem = oKart.getTotalItem();
            $kartDisplayTotalPrice.attr("data-kart-total-price", _totalPrice);
            $kartDisplayTotalItem.attr("data-kart-total-item", _totalItem);
            if (typeof opts.formatTotalPrice === "function" && opts.formatTotalPrice.length > 0) {
                // apply the custom value format
                var _kartTotalPriceText = opts.formatTotalPrice(_totalPrice);
                $kartDisplayTotalPrice.html(_kartTotalPriceText);
            } else {
                $kartDisplayTotalPrice.html(_totalPrice);
            }
        }

        return this;
    };

    var Kart = (function () {
        "use strict";

        var kartItems = [];

        var totalItems = kartItems.length;
        var totalPrice = 0;

        var _updateKart = function () {
            totalItems = kartItems.length;
        };

        var _isPositiveNumber = function (number) {
            return $.isNumeric(number) && (Math.sign(number)>=0);
        };

        var addItem = function (item) {
            kartItems.push(item);
            _updateKart();
        };

        var removeItem = function(attr, value) {
            var i = kartItems.length;
            while(i--){
               if( kartItems[i]
                   && kartItems[i].hasOwnProperty(attr)
                   && (arguments.length === 2 && kartItems[i][attr] === value ) ) {
                   kartItems.splice(i,1);

               }
            }
            _updateKart();
            // return kartItems;
        }

        var getItems = function () {
            return kartItems;
        };

        var getTotalItem = function () {
            return kartItems.length;
        };

        var getTotalPrice = function () {
            return totalPrice;
        }

        var addTotalPrice = function (price) {
            if (_isPositiveNumber(price)) {
                totalPrice += price;
            }
        }

        var subtractTotalPrice = function (price) {
            if (_isPositiveNumber(price)) {
                if (price <= 0) {
                    totalPrice = 0; // make sure the price is never negative
                } else {
                    totalPrice -= price;
                }
            }
        }

        // Public API
        return {
            addItem: addItem,
            removeItem: removeItem,
            getTotalItem: getTotalItem,
            getItems: getItems,
            getTotalPrice: getTotalPrice,
            addTotalPrice: addTotalPrice,
            subtractTotalPrice: subtractTotalPrice
        };

    });

}(jQuery, window);
