/*global $, test, equal */
test("errors should be hidden on keypress", function () {
        $('input').trigger('keypress');
        equal($('.has-error').is(':visible'), true);
});

test("errors not be hidden unless there is a keypress", function(){
    equal($('.has-error').is(':visible'), true);
    $('input').on('keypress', function(){
    $('.has-error').hide()
    })
});

$(document).ready(function(){
    $('input').on('keypress', function(){
        $('.has-error').hide();
    });
});
