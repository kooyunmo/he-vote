const routes = [
  {
    path: ["/", "/home"],
    exact: true,
    component: "Home",
  },
  {
    path: ["/login"],
    exact: true,
    component: "Login",
  },
  {
    path: ["/cast"],
    exact: true,
    component: "Cast"
  },
  {
    path: ["/tally"],
    exact: true,
    component: "Tally",
  },
];

export default routes;
