import { BrowserRouter } from 'react-router-dom';
import '../css/App.css';
import Navbar from './Navbar';
import AppRoutes from '../routes';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <AppRoutes />
    </BrowserRouter>
  );
}

export default App;
