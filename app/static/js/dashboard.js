/*
------------------------------------------------------------
Function to activate form button to open the slider.
------------------------------------------------------------
*/
function open_filters_panel() {
slideIt();
var a = document.getElementById("sidebar");
a.setAttribute("id", "sidebar1");
a.setAttribute("onclick", "close_panel()");
}
/*
------------------------------------------------------------
Function to slide the sidebar form (open form)
------------------------------------------------------------
*/
function slideIt() {
var slidingDiv = document.getElementById("slider");
var stopPosition = 0;
if (parseInt(slidingDiv.style.right) < stopPosition) {
slidingDiv.style.right = parseInt(slidingDiv.style.right) + 2 + "px";
setTimeout(slideIt, 1);
}
}
/*
------------------------------------------------------------
Function to activate form button to close the slider.
------------------------------------------------------------
*/
function close_panel() {
slideIn();
a = document.getElementById("sidebar1");
a.setAttribute("id", "sidebar");
a.setAttribute("onclick", "open_filters_panel()");
}
/*
------------------------------------------------------------
Function to slide the sidebar form (slide in form)
------------------------------------------------------------
*/
function slideIn() {
var slidingDiv = document.getElementById("slider");
var stopPosition = -342;
if (parseInt(slidingDiv.style.right) > stopPosition) {
slidingDiv.style.right = parseInt(slidingDiv.style.right) - 2 + "px";
setTimeout(slideIn, 1);
}
}


/*
--------------------------------------------------------------
Set listeners on sliders to change value when sliders move
--------------------------------------------------------------
*/

//Energy Slider
var energy_slider = document.getElementById("energy_level");
var enrgy_label = document.getElementById("energy_level_label");
// enrgy_label.innerHTML = slider.value;

energy_slider.oninput = function() {
  enrgy_label.innerHTML = this.value/100;
}

//Sound Quality slider
var sound_quality_slider = document.getElementById("sound_quality");
var sound_quality_label = document.getElementById("sound_quality_label");
// enrgy_label.innerHTML = slider.value;

sound_quality_slider.oninput = function() {
  sound_quality_label.innerHTML = this.value/100;
}


//Danceability slider
var danceability_slider = document.getElementById("danceability");
var danceability_label = document.getElementById("danceability_label");
// enrgy_label.innerHTML = slider.value;

danceability_slider.oninput = function() {
  danceability_label.innerHTML = this.value/100;
}

//Valence slider
var valence_slider = document.getElementById("valence");
var valence_label = document.getElementById("valence_label");
// enrgy_label.innerHTML = slider.value;

valence_slider.oninput = function() {
  valence_label.innerHTML = this.value/100;
}

//Loudness slider
var loudness_slider = document.getElementById("loudness");
var loudness_label = document.getElementById("loudness_label");
// enrgy_label.innerHTML = slider.value;

loudness_slider.oninput = function() {
  loudness_label.innerHTML = this.value/100;
}

//Instrumentalness slider
var instrumentalness_slider = document.getElementById("instrumentalness");
var instrumentalness_label = document.getElementById("instrumentalness_label");
// enrgy_label.innerHTML = slider.value;

instrumentalness_slider.oninput = function() {
  instrumentalness_label.innerHTML = this.value/100;
}


/*
--------------------------------------------------
Custom SELECT
---------------------------------------------------
*/

var x, i, j, selElmnt, a, b, c;
/*look for any elements with the class "custom-select":*/
x = document.getElementsByClassName("custom-select");
for (i = 0; i < x.length; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  /*for each element, create a new DIV that will act as the selected item:*/
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /*for each element, create a new DIV that will contain the option list:*/
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 0; j < selElmnt.length; j++) {
    /*for each option in the original select element,
    create a new DIV that will act as an option item:*/
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /*when an item is clicked, update the original select box,
        and the selected item:*/
        var y, i, k, s, h;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        h = this.parentNode.previousSibling;
        for (i = 0; i < s.length; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            for (k = 0; k < y.length; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
      /*when the select box is clicked, close any other select boxes,
      and open/close the current select box:*/
      e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });
}
function closeAllSelect(elmnt) {
  /*a function that will close all select boxes in the document,
  except the current select box:*/
  var x, y, i, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  for (i = 0; i < y.length; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < x.length; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);
