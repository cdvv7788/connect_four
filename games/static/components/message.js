function Message(props) {
  return React.createElement(
    "div",
    { className: "text-center p-4" },
    props.message
  );
}
