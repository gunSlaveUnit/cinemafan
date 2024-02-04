import React from 'react';

import {
  RouterProvider,
  createBrowserRouter,
} from 'react-router-dom';

import Home from './Home'
import Movies from './Movies'

const router = createBrowserRouter(
  [
    {
      path: "/",
      element: <Home />,
    },
    {
      path: "/movies",
      element: <Movies />,
    },
  ]
)

const App = () => {
  return (
    <div>
      <header></header>

      <main>
        <RouterProvider router={router} />
      </main>

      <footer></footer>
    </div>
  )
}

export default App;
