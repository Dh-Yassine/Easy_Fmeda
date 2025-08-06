import React, { useRef } from "react";

export default function RippleButton({ children, className = "", style = {}, ...props }) {
  const btnRef = useRef(null);

  const createRipple = (event) => {
    const button = btnRef.current;
    if (!button) return;
    const circle = document.createElement("span");
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    circle.className = "ripple";
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.getBoundingClientRect().left - radius}px`;
    circle.style.top = `${event.clientY - button.getBoundingClientRect().top - radius}px`;
    button.appendChild(circle);
    circle.addEventListener('animationend', () => {
      circle.remove();
    });
  };

  return (
    <button
      ref={btnRef}
      className={className}
      style={style}
      {...props}
      onClick={e => {
        createRipple(e);
        if (props.onClick) props.onClick(e);
      }}
    >
      {children}
    </button>
  );
}