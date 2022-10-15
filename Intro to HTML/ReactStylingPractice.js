//Create a React app from scratch.
//Show a single h1 that says "Good morning" if between midnight and 12PM.
//or "Good Afternoon" if between 12PM and 6PM.
//or "Good evening" if between 6PM and midnight.
//Apply the "heading" style in the styles.css
//Dynamically change the color of the h1 using inline css styles.
//Morning = red, Afternoon = green, Night = blue.
import React from "react";
import ReactDom from "react-dom";

const date = new Date(2019, 1, 1, 20).getHours();

const timeOfDay = {
  date: "Morning",
  color: "red"
};

if (date >= 0 && date <= 12) {
  timeOfDay.date = "Morning";
  timeOfDay.color = "red";
} else if (date > 12 && date < 18) {
  timeOfDay.date = "Afternoon";
  timeOfDay.color = "green";
} else {
  timeOfDay.date = "Night";
  timeOfDay.color = "blue";
}

ReactDom.render(
  <h1 className="heading" style={timeOfDay}>Good {timeOfDay.date}</h1>,
  document.getElementById("root")
);
