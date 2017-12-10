var img_1, img_2;
var img_1_src, img_2_src;
//var descript_1, descript_2;
var category = 2;
var loaded_image_number = 0;
var q1, q2;
var detail_state = 0;
var image_state = [];
var mode = "training";

$.ajaxSetup({
  contentType: "application/json; charset=utf-8"
});

function image_loaded() {

    loaded_image_number = loaded_image_number + 1;

    if (loaded_image_number == 2) {
        $("#pic_overlay_1").hide();
        $("#pic_overlay_2").hide();
        $("#picture_1").css("opacity", "1");
        $("#picture_2").css("opacity", "2");
        $("#name_1").css("color", "#000000");
        $("#name_1").css("font-weight", "normal");
        $("#name_2").css("color", "#000000");
        $("#name_2").css("font-weight", "normal");

        $("#name_1").text("");
        $("#name_2").text("");

        $(".loading").hide();
        $("#name_1").show();
        $("#name_2").show();

        $("#picture_1").parent().addClass("loaded");
    }
}

function get_select_items(){
    var selected = [];
    for(var i = 0; i < 10; i ++){
        if(image_state[i] === 1){
            selected.push(i);
        }
    }
    return selected;
}
function update_pair(data, status) {
    var JSONobj = data;
    console.log(JSONobj);
    var urls = JSONobj.urls;
    mode = JSONobj.mode;

    if(mode === "training"){
        $("#move-wrapper").hide();
        if(urls.length === 10){
            $("#game").hide();
            $("#yuck-wrapper").hide();
            $("#ten-game").show();
            for(var i = 0; i < 10; i ++){
                $("#candidate_" + String(i + 1)).attr("src", urls[i]);
                image_state[i] = 0;
                $("#candidate_" + String(i + 1)).css("border-color", "");
                $("#candidate_" + String(i + 1)).css("border-width", "");
            }
        } else {
            $("#ten-game").hide();
            $("#game").show();
            $("#yuck-wrapper").show();
            if ($("#picture_1").parent().hasClass("loaded")) {
                $("#picture_1").parent().removeClass("loaded");
            }
            loaded_image_number = 0;
            $("#picture_1").attr("src", urls[0]);
            $("#picture_2").attr("src", urls[1]);

            $("#name_1").hide();
            $("#name_2").hide();
            $(".loading").show();
        }
    } else if (mode === "testing") {
        $("#ten-game").hide();
        $("#game").hide();
        $("#suggestion").show();
        window.scrollTo(0, 0);
        for(var i = 0; i < 20; i ++){
            $("#suggestion_" + String(i + 1)).attr("src", urls[i]);
            $("#suggestion_" + String(i + 1)).css("border-color", "");
            $("#suggestion_" + String(i + 1)).css("border-width", "");
            var start_index = urls[i].indexOf("amazonaws.com/");
            $("#suggestion_" + String(i + 1)).wrap("<a href=\"http://www.yummly.com/recipe/" + urls[i].substring(start_index + 14, urls[i].length - 4) + "\" target=\"_blank\"></a>");
        }
        //$("#yuck-wrapper").hide();
        //$("#move-wrapper").show();
        //$("#two-instruction-2").html("");
        //$("#two-instruction-2").css("color", "#AB3535");

        /*
        if ($("#picture_1").parent().hasClass("loaded")) {
            $("#picture_1").parent().removeClass("loaded");
        }

        loaded_image_number = 0;
        $("#picture_1").attr("src", urls[0]);
        $("#picture_2").attr("src", urls[1]);

        $("#name_1").hide();
        $("#name_2").hide();
        $(".loading").show();
        */
        /*
        $("#game").hide();
        $("#ten-game").show();
        $("#ten-instruction-1").html("Compare the images below and tap on FIVE food items that you like most.");
        $("#ten-instruction-2").html("");
        for(var i = 0; i < 10; i ++){
            $("#candidate_" + String(i + 1)).attr("src", urls[i]);
            image_state[i] = 0;
            $("#candidate_" + String(i + 1)).css("border-color", "");
            $("#candidate_" + String(i + 1)).css("border-width", "");
        }
        */
    }

    /*
    if (JSONobj.previous_image_index) {
        if (JSONobj.previous_image_number == "9999") {
            $("#progress" + JSONobj.previous_image_index).attr("src", "webImage/yuck.jpg");
        } else {
            $("#progress" + JSONobj.previous_image_index).attr("src", JSONobj.previous_image_src);
        }
    }

    if (JSONobj.first) {
        if ($("#picture_1").parent().hasClass("loaded")) {
            $("#picture_1").parent().removeClass("loaded");
        }
        loaded_image_number = 0;
        $("#picture_1").attr("src", JSONobj.src_1);
        $("#picture_2").attr("src", JSONobj.src_2);

        descript_1 = JSONobj.description_1;
        descript_2 = JSONobj.description_2;

        img_1 = JSONobj.first;
        img_2 = JSONobj.second;
        img_1_src = JSONobj.src_1;
        img_2_src = JSONobj.src_2;
        $("#name_1").hide();
        $("#name_2").hide();
        $(".loading").show();
    }

    if (JSONobj.statistic) {

        $(".game").hide();
        $(".after-survey").slideDown();

        var positive_array = get_mean_array(JSONobj.statistic.positive);
        var negative_array = get_mean_array(JSONobj.statistic.negative);
        var positive_error = get_error_array(JSONobj.statistic.positive);
        var negative_error = get_error_array(JSONobj.statistic.negative);

        var categories = ['FASAT', 'GLUS', 'FAMS', 'FAT',
            'PROCNT', 'STARCH', 'CA', 'NA', 'ZN',
            'VITC', 'MN', 'K', 'Piquant', 'Bitter',
            'Sweet', 'Meaty', 'Salty', 'Sour'];
        generate_spiderweb("chart-1", positive_array.slice(0, 6), positive_error.slice(0, 6),
            negative_array.slice(0, 6), negative_error.slice(0, 6), categories.slice(0, 6), false);
        generate_spiderweb("chart-2", positive_array.slice(6, 12), positive_error.slice(6, 12),
            negative_array.slice(6, 12), negative_error.slice(6, 12), categories.slice(6, 12), false);
        generate_spiderweb("chart-3", positive_array.slice(12, 18), positive_error.slice(12, 18),
            negative_array.slice(12, 18), negative_error.slice(12, 18), categories.slice(12, 18), true);

        var maxValue = get_max_remark_value(JSONobj.statistic.posiRemark, JSONobj.statistic.negaRemark);

        $("#remark").html(JSONobj.statistic.remark);
        image_circle_draw("#positive", JSONobj.statistic.posiRemark, maxValue, "#68C8E8");
        image_circle_draw("#negative", JSONobj.statistic.negaRemark, maxValue, "#EDBE58");

        $(".game-feed").show();

    }
    */
}

function normalize_vector(vector){

    var max_val = Math.abs(vector[0]);
    for(var i = 1; i < vector.length; i ++){
        if(Math.abs(vector[i]) > max_val){
            max_val = Math.abs(vector[i]);
        }
    }

    for(var i = 0; i < vector.length; i ++){
        vector[i] = vector[i]/max_val;
    }

    return vector;

}

function get_max_remark_value(original_posi, original_nega){

    var max = 0;

    for(var i = 0; i < original_posi.length; i ++){
        if(parseFloat(original_posi[i].remarkValue) > max){
            max = parseFloat(original_posi[i].remarkValue);
        }
    }

    for(var i = 0; i < original_nega.length; i ++){
        if(parseFloat(original_nega[i].remarkValue) > max){
            max = parseFloat(original_nega[i].remarkValue);
        }
    }

    return max;
}

function image_circle_draw(div_id, original_array, maxValue, color){

    for(var i = 0; i < original_array.length; i ++){
        var ratio = parseFloat(original_array[i].remarkValue) / maxValue;

        if(ratio > 0.1){
            $(div_id).append(getImageElement(original_array[i].imgSrc));
            $(div_id).append(getCircleElement(ratio, color, parseFloat(original_array[i].remarkValue)));
        }

    }
}

function get_mean_array(original_array) {
    var new_array = new Array(18);

    new_array[0] = parseFloat(original_array.FASAT);
    new_array[1] = parseFloat(original_array.GLUS);
    new_array[2] = parseFloat(original_array.FAMS);
    new_array[3] = parseFloat(original_array.FAT);
    new_array[4] = parseFloat(original_array.PROCNT);
    new_array[5] = parseFloat(original_array.STARCH);

    new_array[6] = parseFloat(original_array.CA);
    new_array[7] = parseFloat(original_array.NA);
    new_array[8] = parseFloat(original_array.ZN);
    new_array[9] = parseFloat(original_array.VITC);
    new_array[10] = parseFloat(original_array.MN);
    new_array[11] = parseFloat(original_array.K);

    new_array[12] = parseFloat(original_array.Piquant);
    new_array[13] = parseFloat(original_array.Bitter);
    new_array[14] = parseFloat(original_array.Sweet);
    new_array[15] = parseFloat(original_array.Meaty);
    new_array[16] = parseFloat(original_array.Salty);
    new_array[17] = parseFloat(original_array.Sour);

    return new_array;
}

function get_error_array(original_array){
    var new_array = new Array(18);

    new_array[0] = parseFloat(original_array.FASAT_E);
    new_array[1] = parseFloat(original_array.GLUS_E);
    new_array[2] = parseFloat(original_array.FAMS_E);
    new_array[3] = parseFloat(original_array.FAT_E);
    new_array[4] = parseFloat(original_array.PROCNT_E);
    new_array[5] = parseFloat(original_array.STARCH_E);

    new_array[6] = parseFloat(original_array.CA_E);
    new_array[7] = parseFloat(original_array.NA_E);
    new_array[8] = parseFloat(original_array.ZN_E);
    new_array[9] = parseFloat(original_array.VITC_E);
    new_array[10] = parseFloat(original_array.MN_E);
    new_array[11] = parseFloat(original_array.K_E);

    new_array[12] = parseFloat(original_array.Piquant_E);
    new_array[13] = parseFloat(original_array.Bitter_E);
    new_array[14] = parseFloat(original_array.Sweet_E);
    new_array[15] = parseFloat(original_array.Meaty_E);
    new_array[16] = parseFloat(original_array.Salty_E);
    new_array[17] = parseFloat(original_array.Sour_E);

    return new_array;
}

function clear_progress() {

    var i;
    for (i = 1; i <= 10; i++) {
        $("#progress" + i).attr("src", "webImage/empty.jpg");
    }
}

function get_datetime() {
    var dayObject = new Date();

    return dayObject.getFullYear() + "-" +
            (dayObject.getMonth() + 1) + "-" +
            dayObject.getDate() + " " +
            dayObject.getHours() + ":" +
            dayObject.getMinutes() + ":" +
            dayObject.getSeconds() + "." + dayObject.getMilliseconds();
}

function clear_nav() {
    $("#breakfast").attr("class", "");
    $("#lunch").attr("class", "");
    $("#snack").attr("class", "");
}

function check_logout(data, status) {
    if (data == "success") {
        window.location.href = "index.html";
    }
}

function get_evaluate_choice(){

    var radios_match = document.getElementsByName("match");
    var radios_fun = document.getElementsByName("fun");

    for(var i = 0; i < radios_match.length; i ++){
        if(radios_match[i].checked){
            q1 = parseInt(radios_match[i].value);
            break;
        }
    }

    for(var i = 0; i < radios_fun.length; i ++){
        if(radios_fun[i].checked){
            q2 = parseInt(radios_fun[i].value);
            break;
        }
    }

}

function direct_web(data, status){

    var json_obj = JSON.parse(data);

    if(json_obj.web == "survey"){
        window.location.href = "survey.html";
    } else if (json_obj.web == "final"){
        window.location.href = "finalpage.html";
    }
}

function clear_image_all(){
    for(var i = 0; i < 10; i ++){
        $("#candidate_" + String(i + 1)).attr("src", "webImage/empty.jpg");
        $("#candidate_" + String(i + 1)).css("opacity", "1");
        //$("#candidate_" + String(i + 1)).css("border-color", "");
        //$("#candidate_" + String(i + 1)).css("border-width", "");
        $("#overlay_" + String(i + 1)).hide();
    }
}

$(document).ready(function () {
  // drag and drop
  (function () {
  'use strict';
    function handleStart (e) {
      dragFrom = e.target;
    }

    function handleDrop (index, e) {
      function onDragOver (e) {
        dragTo = e.target;
        var $from = $(dragFrom);
        var $p = $from.parent();
        result[index].push($from.attr('id'));
        $p.remove();
        $('#remainResult').text(--remaining);
        if(remaining == 0){
            console.log(result);
            $.post("/result", JSON.stringify({
                "yummy": result[0],
                "noway": result[1]
            }),function(){
                window.location.href = "final.html";
            });
        }
      }
      e.preventDefault();
      e.stopPropagation();
      onDragOver(e);
    }
    function handleDragOver (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    var dragFrom;
    var dragTo;
    var remaining = 20;
    var $buckets = $('.item-container');
    var $imgs = $('img');
    var result = [
      [],
      []
    ];
    var dragTargets = [
      $buckets.eq(0),
      $buckets.eq(1),
    ];

    $imgs.toArray().forEach(function (e) {
      e.addEventListener('dragstart', handleStart, false);
    });

    $buckets.toArray().forEach(function (e, i) {
      e.addEventListener('dragover', handleDragOver, false);
      e.addEventListener('drop', handleDrop.bind(e, i), false);
    });
  })();

    $(".loading").hide();
    $("#move-wrapper").hide();

    $.post("/update", {
    },update_pair);

    $("#picture_1").mousedown(function () {
        $("#name_1").css("color", "#6ADE2F");
        $("#name_1").css("font-weight", "bold");
        $("#name_1").text("Yum!");
        $("#picture_1").css("opacity", "0.15");

    });

    $("#picture_1").click(function () {
        $.post("/update", JSON.stringify({
            choice: [0]
        }), update_pair);
        $("#pic_overlay_1").show();
        //window.scrollTo(0, 0);
    });

    $("#submit-ten").click(function (){
        var current_choices = get_select_items();
        if(mode === "testing" && current_choices.length !== 5){
            $("#ten-instruction-2").html("Please select exact FIVE items!");
            $("#ten-instruction-2").css("color", "#AB3535");
        } else {
            $.post("/update", JSON.stringify({
                choice: current_choices
            }), update_pair);
            clear_image_all();
        }
        window.scrollTo(0, 0);
    });

    $("#picture_1").load(image_loaded);

    $("#picture_2").load(image_loaded);

    $("#picture_2").mousedown(function () {
        $("#name_2").css("color", "#6ADE2F");
        $("#name_2").css("font-weight", "bold");
        $("#name_2").text("Yum!");
        $("#picture_2").css("opacity", "0.15");

    });

    $("#picture_2").click(function () {
        //$("#name_2").css("color", "#6ADE2F");
        //$("#name_2").text("Yum!");
        $.post("/update", JSON.stringify({
            choice: [1]
        }), update_pair);
        $("#pic_overlay_2").show();
        //window.scrollTo(0, 0);
    });

    $(".yuck").click(function () {
        $.post("/update", JSON.stringify({
            choice: []
        }), update_pair);
    });

    for(var i = 0; i < 10; i ++){
        image_state[i] = 0;

        $("#candidate_" + String(i + 1)).click(function(){
            var index = this.id.substring(10);
            if(image_state[index - 1] === 0){
                $("#overlay_" + String(index)).show();
                $("#candidate_" + String(index)).css("opacity", "0.15");
                //$("#candidate_" + String(index)).css("border-color", "#F7B543");
                //$("#candidate_" + String(index)).css("border-width", "2px");
                image_state[index - 1] = 1;
                //console.log(image_state);
            } else {
                $("#overlay_" + String(index)).hide();
                $("#candidate_" + String(index)).css("opacity", "1");
                //$("#candidate_" + String(index)).css("border-color", "");
                //$("#candidate_" + String(index)).css("border-width", "");
                image_state[index - 1] = 0;
                //console.log(image_state);
            }
        });

        $("#overlay_" + String(i + 1)).click(function(){
            var index = this.id.substring(8);
            if(image_state[index - 1] === 0){
                $("#overlay_" + String(index)).show();
                $("#candidate_" + String(index)).css("opacity", "0.15");
                //$("#candidate_" + String(index)).css("border-color", "#F7B543");
                //$("#candidate_" + String(index)).css("border-width", "2px");
                image_state[index - 1] = 1;
                //console.log(image_state);
            } else {
                $("#overlay_" + String(index)).hide();
                $("#candidate_" + String(index)).css("opacity", "1");
                //$("#candidate_" + String(index)).css("border-color", "");
                //$("#candidate_" + String(index)).css("border-width", "");
                image_state[index - 1] = 0;
                //console.log(image_state);
            }
        });
    }
    //console.log(image_state);
});
