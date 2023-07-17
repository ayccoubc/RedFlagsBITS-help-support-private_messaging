function hide_or_show_div(div) {
  var x = document.getElementById(div);
  if (x.style.display === "none") {
    x.style.display = "inline-block";
  } else {
    x.style.display = "none";
  }
}

function Enable_Submit(id) {
  var x = document.getElementById(id);
  x.disabled = false;
}

function Toggle_Enable_Submit(id) {
  var x = document.getElementById(id);
  x.disabled = !x.disabled;
}