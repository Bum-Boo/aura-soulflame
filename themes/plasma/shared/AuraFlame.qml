import QtQuick

Canvas {
    onPaint: {
        const c = getContext("2d");
        c.reset();
        c.scale(width / 40, height / 60);

        const glow = c.createRadialGradient(20, 35, 3, 20, 35, 22);
        glow.addColorStop(0, "#6390E9D7");
        glow.addColorStop(1, "#0090E9D7");
        c.fillStyle = glow;
        c.fillRect(0, 0, 40, 60);

        const mint = c.createLinearGradient(11, 46, 28, 10);
        mint.addColorStop(0, "#49C6AE");
        mint.addColorStop(0.5, "#90E9D7");
        mint.addColorStop(1, "#DEFFF2");
        c.fillStyle = mint;
        c.beginPath();
        c.moveTo(19, 51);
        c.bezierCurveTo(5, 49, 6, 37, 13, 29);
        c.bezierCurveTo(17, 24, 21, 22, 21, 11);
        c.bezierCurveTo(32, 19, 24, 25, 29, 30);
        c.bezierCurveTo(32, 28, 32, 26, 32, 24);
        c.bezierCurveTo(41, 40, 29, 54, 19, 51);
        c.fill();

        c.fillStyle = "#DBFFF0";
        c.beginPath();
        c.moveTo(20, 48);
        c.bezierCurveTo(14, 47, 14, 42, 20, 37);
        c.bezierCurveTo(22, 35, 24, 32, 23, 29);
        c.bezierCurveTo(31, 38, 27, 48, 20, 48);
        c.fill();
    }
}
