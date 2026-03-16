import LoginForm from '../components/forms/login-form';

interface LoginPageProps {
  onLogin: () => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  return <LoginForm onLogin={onLogin} />;
}
