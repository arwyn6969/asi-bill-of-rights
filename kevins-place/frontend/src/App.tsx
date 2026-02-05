import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { TelegramAuthWrapper } from './components/TelegramAuthWrapper';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { ZoneView } from './pages/ZoneView';
import { ThreadView } from './pages/ThreadView';
import { Search } from './pages/Search';

function App() {
  return (
    <BrowserRouter>
      <TelegramAuthWrapper>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="zone/:id" element={<ZoneView />} />
            <Route path="thread/:id" element={<ThreadView />} />
            <Route path="search" element={<Search />} />
          </Route>
        </Routes>
      </TelegramAuthWrapper>
    </BrowserRouter>
  );
}

export default App;
