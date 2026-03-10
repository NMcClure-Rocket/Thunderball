import { render, screen } from '@testing-library/react';
import { Button } from '../../src/components/Button';

describe('Button Component', () => {
  it('renders button with label', () => {
    const handleClick = jest.fn();
    render(<Button label="Click Me" onClick={handleClick} />);
    
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Click Me" onClick={handleClick} />);
    
    screen.getByText('Click Me').click();
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
