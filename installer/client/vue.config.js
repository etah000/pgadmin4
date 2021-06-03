module.exports = {
    publicPath: './',
    pluginOptions: {
        electronBuilder: {
            nodeIntegration: true,
            // List native deps here if they don't work
            //externals: ['app'],
            // If you are using Yarn Workspaces, you may have multiple node_modules folders
            // List them all here so that VCP Electron Builder can find them
            nodeModulesPath: ['./node_modules'],
            builderOptions: {
                "appId": "com.snowball.app",
                "asar": false,
                "asarUnpack": [
                    "app",
                    "background.js"
                ],
                //"compression": "store", // "store" | "normal"| "maximum" 打包压缩情况(store 相对较快)，store 39749kb, maximum 39186kb
                //"extraResources": ["./extraResources/**"],
                "extraResources":  [{ // 拷贝app等静态文件到指定位置
                    "from": "./extraResources/app",
                    "to": "./app/app"
                },{ // 拷贝app等静态文件到指定位置
                    "from": "./extraResources/app.exe",
                    "to": "./app/app.exe"
                }],
                productName: "snowball-installer",//项目名，也是生成的安装文件名
                copyright: "Copyright © 2021",//版权信息
                directories: {
                    output: "./dist_electron"//输出文件路径
                },
                mac:{
                    "target": [
                        "dmg",
                        "pkg"
                    ]
                },
                /*"files": [
                    "dist/",
                    "node_modules/",
                    "index.html",
                    "main.js",
                    "package.json",
                    "renderer.js",
                    "styles.css",
                    "visitor.py",
                    "download.py"
                ],
*/
               /* "dmg": {
                    "contents": [
                        {
                            "x": 110,
                            "y": 150
                        },
                        {
                            "x": 240,
                            "y": 150,
                            "type": "link",
                            "path": "/Applications"
                        }
                    ]
                },*/
                "linux": {
                    "target": [
                        "AppImage",
                        "deb"
                    ]
                },/*
                "win": {
                    "target": "squirrel",
                    "icon": "build/icon.ico"
                },*/
                win: {//win相关配置
                    icon: "./public/pgAdmin4.ico",//图标，当前图标在根目录下，注意这里有两个坑
                    target: [
                        {
                            target: "nsis",//利用nsis制作安装程序
                            arch: [
                                "x64",//64位
                            ]
                        }
                    ]
                },
                nsis: {
                    oneClick: false, // 是否一键安装
                    allowElevation: true, // 允许请求提升。 如果为false，则用户必须使用提升的权限重新启动安装程序。
                    allowToChangeInstallationDirectory: true, // 允许修改安装目录
                    installerIcon: "./public/pgAdmin4.ico",// 安装图标
                    uninstallerIcon: "./public/pgAdmin4.ico",//卸载图标
                    installerHeaderIcon: "./public/pgAdmin4.ico", // 安装时头部图标
                    createDesktopShortcut: true, // 创建桌面图标
                    createStartMenuShortcut: true,// 创建开始菜单图标
                    shortcutName: "pgAdmin4", // 图标名称
                },
            }
        }
    }
}