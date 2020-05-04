function Message(props) {
  return React.createElement(
    "div",
    { className: `text-center p-4 text-${props.messageColor}-600` },
    props.message
  );
}
