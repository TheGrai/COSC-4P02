import "./App.css";
import { Route, Routes } from "react-router-dom";
import { Home } from "./pages/Home";
import { HomeCG } from "./pages/HomeCG";
import { Chat } from "./pages/Chat";
import { ChatCG} from "./pages/ChatCG";
import { useState } from "react";

function App() {
  const [name, setName] = useState("");

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  return (
    <div className="App" id="mainApp">
      <Routes>
        <Route
          path="/"
          element={<Home name={name} handleNameChange={handleNameChange} />}
        />
        <Route path="/chat" element={<Chat name={name} />} />
        <Route path="/chatCG" element={<ChatCG name={name} />} />
        <Route path="/homeCG" element={<HomeCG name={name} handleNameChange={handleNameChange}/>}
        />
      </Routes>
    </div>
  );
}

export default App;
