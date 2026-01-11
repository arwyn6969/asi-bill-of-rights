import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { ZoneView } from './pages/ZoneView';
import { ThreadView } from './pages/ThreadView';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="zone/:id" element={<ZoneView />} />
          <Route path="thread/:id" element={<ThreadView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
