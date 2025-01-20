window.dash_clientside = window.dash_clientside || {};

window.dash_clientside.addDropZone = {
    dropZoneGrid2GridSimple: async function (gridIdLeft, gridIdRight) {
        // Get the grids APIs
        const gridLeftAPI = await dash_ag_grid.getApiAsync(gridIdLeft);
        const gridRightAPI = await dash_ag_grid.getApiAsync(gridIdRight);

        // Get the dropzones parameters from each grid
        const gridLeftDropZone = gridLeftAPI.getRowDropZoneParams();
        const gridRightDropZone = gridRightAPI.getRowDropZoneParams();

        // Add RIGHT grid as dropzone of LEFT grid
        gridLeftAPI.addRowDropZone(gridRightDropZone);
        // Add LEFT grid as dropzone of RIGHT grid
        gridRightAPI.addRowDropZone(gridLeftDropZone);

        return window.dash_clientside.no_update
    },
}