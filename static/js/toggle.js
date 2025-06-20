function hasClass(ele, cls) {
  return ele.className.match(new RegExp("(\\s|^)" + cls + "(\\s|$)"));
}

function addClass(ele, cls) {
  if (!this.hasClass(ele, cls)) ele.className += cls;
}

function removeClass(ele, cls) {
  if (hasClass(ele, cls)) {
    const reg = new RegExp("(\\s|^)" + cls + "(\\s|$)");
    ele.className = ele.className.replace(reg, "");
  }
}

function removeAllClass(ele) {
  ele.className = "";
}

function replaceClass(ele, oldClass, newClass) {
  if (hasClass(ele, oldClass)) {
    removeClass(ele, oldClass);
    addClass(ele, newClass);
  }
}

function toggleClass(ele, cls1, cls2) {
  if (hasClass(ele, cls1)) {
    replaceClass(ele, cls1, cls2);
  } else if (hasClass(ele, cls2)) {
    replaceClass(ele, cls2, cls1);
  } else {
    addClass(ele, cls1);
  }
}

function toggleVisibility(id) {
  const x = document.getElementById(id);
  toggleClass(x, "hide", "show");
}

function toggleTheme(id) {
  const x = document.getElementById(id);
  toggleClass(x, "light", "dark");

  // if (body.classList.contains("dark")) {
  //   body.querySelector(".mode-text").innerText = "Light Mode";
  // } else {
  //   body.querySelector(".mode-text").innerText = "Dark Mode";
  // }
}

// For Multiple Themes (Future Plan)
function turnOnTheme(id, theme) {
  const x = document.getElementById(id);
  removeAllClass(x);
  addClass(x, theme);
}

const body = document.querySelector("body");
sidebar = body.querySelector(".sidebar");
toggle = body.querySelector(".toggle");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");

  // if (body.classList.contains("dark")) {
  //   body.querySelector(".mode-text").innerText = "Light Mode";
  // } else {
  //   body.querySelector(".mode-text").innerText = "Dark Mode";
  // }
});
