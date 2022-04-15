import './App.css';
import React from "react"
import { useState } from "react";
import BUChat from "./BUChat";
import CGChat from "./CGChat";

const styles = {
  button1: {
    backgroundColor: "#5683d6",
    borderColor: "#1D2129",
    borderStyle: "solid",
    borderRadius: 20,
    borderWidth: 2,
    color: "#1D2129",
    fontSize: 18,
    fontWeight: "300",
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 16,
    paddingRight: 16,
    outline: "none"
  },
  button2: {
    backgroundColor: "#f77c7c",
    borderColor: "#1D2129",
    borderStyle: "solid",
    borderRadius: 20,
    borderWidth: 2,
    color: "#1D2129",
    fontSize: 18,
    fontWeight: "300",
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 16,
    paddingRight: 16,
    outline: "none"
  },
  chatTitle: {

    fontSize: 18,
    fontWeight: "bold"

  }

}

function App() {
  const [isBrock, setVersion] = useState(false);

  return (
    <div className="App">
        <div class="switchButton">
          {isBrock ? <button style = {styles.button1} onClick={() => setVersion(!isBrock)}>Switch Version</button>
                  :<button style = {styles.button2} onClick={() => setVersion(!isBrock)}>Switch Version</button>}
        </div>
        { isBrock ? <BrockCB />:<CanadaGamesCB/>}
    </div>
  );
}

function BrockCB() {

  //document.body.style.backgroundColor = '#ed9a9a';
  document.body.classList.add("bu");
  document.body.classList.remove("cg");

  return (
    <div> 
      <img src = "brocku.png" height = "75"/>
      <BUChat />
    </div>
    
  )
}

function CanadaGamesCB() {

  //document.body.style.backgroundColor = '#abc5f5';
  document.body.classList.add("cg");
  document.body.classList.remove("bu");

  return (
    <div> 
      <img src = "canada games.png" height = "75"/>
      <CGChat />
    </div>
  )
}
export default App;
