import "./App.css";
import { Route, Routes } from "react-router-dom";
import { Home } from "./pages/Home";
import { Chat } from "./pages/Chat";
import { useState } from "react";

function App() {
  const [name, setName] = useState("");

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  return (
    <div className="App">
      <Routes>
        <Route
          path="/"
          element={<Home name={name} handleNameChange={handleNameChange} />}
        />
        <Route path="/chat" element={<Chat name={name} />} />
      </Routes>
    </div>
  );
}

export default App;
