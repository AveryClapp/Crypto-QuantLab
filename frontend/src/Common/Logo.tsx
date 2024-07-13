import React from "react";

interface IconProps {
  name: string;
  className?: string;
}

const Icon: React.FC<IconProps> = ({ name, className }) => (
  <svg className={className}>
    <use xlinkHref={`#icon-${name}`} />
  </svg>
);

export default Icon;
