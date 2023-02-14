import { Theme, createTheme } from "@mui/material/styles";

export const themeDark: Theme = createTheme({
    palette: {
        mode: "dark",
        primary: {
            main: "#ab47bc",
        },
        secondary: {
            main: "#263238",
        },
    },
});
