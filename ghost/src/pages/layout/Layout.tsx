import {
    Button,
    Grid,
    Paper,
    Stack,
    Typography,
    useMediaQuery,
    useTheme,
} from "@mui/material";
import { Box } from "@mui/system";
import { Outlet } from "react-router-dom";
import "./style.scss";
import { GiGhost } from "react-icons/gi";
import { MdDownload, MdLogin, MdSearch } from "react-icons/md";
import { useTranslation } from "react-i18next";

export function Layout() {
    const theme = useTheme();
    const { t } = useTranslation();
    const isXs = useMediaQuery("(max-width: 600px)");
    return (
        <Box
            className="layout"
            sx={{ backgroundColor: theme.palette.background.default }}
        >
            <Box className="header">
                <Grid container spacing={1}>
                    <Grid item md={3} sm={5} xs={7}>
                        <Paper className="header-item title">
                            <Stack spacing={2} direction="row">
                                <GiGhost size={30} className="icon" />
                                <Typography
                                    variant="overline"
                                    className="app-name"
                                >
                                    Ghost
                                </Typography>
                            </Stack>
                        </Paper>
                    </Grid>
                    {!isXs && (
                        <Grid item md={7} sm={2} xs={0}>
                            <></>
                        </Grid>
                    )}
                    <Grid item md={2} sm={5} xs={5}>
                        <Button
                            variant="outlined"
                            className="header-item button"
                            startIcon={<MdLogin />}
                        >
                            {t("account.login")}
                        </Button>
                    </Grid>
                </Grid>
            </Box>
            <Box className="content">
                <Outlet />
            </Box>
        </Box>
    );
}
