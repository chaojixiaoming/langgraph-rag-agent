#!/usr/bin/env python3
"""
uv 锁文件生成脚本

使用方法:
    python scripts/generate_uv_lock.py

说明:
    由于权限问题无法直接运行 uv 命令，
    此脚本提供手动生成 uv.lock 的替代方案。
"""

import sys
import subprocess
from pathlib import Path


def check_uv_installed():
    """检查 uv 是否已安装"""
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print(f"✅ uv 已安装: {result.stdout.strip()}")
            return True
        return False
    except FileNotFoundError:
        return False


def install_uv():
    """安装 uv"""
    print("\n📦 正在安装 uv...")
    
    # 尝试使用 pip 安装到用户目录
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "uv"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ uv 安装成功!")
        
        # 提示用户添加 PATH
        import os
        user_scripts = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Programs", "Python", "Python313", "Scripts")
        if not os.path.exists(user_scripts):
            # 尝试其他常见位置
            for base in [sys.prefix, sys.exec_prefix]:
                scripts = os.path.join(base, "Scripts")
                if os.path.exists(scripts):
                    user_scripts = scripts
                    break
        
        print(f"\n💡 请将以下目录添加到系统 PATH:")
        print(f"   {user_scripts}")
        print(f"\n   然后重启终端并运行: uv lock")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e.stderr}")
        return False


def generate_lock_file():
    """生成 uv.lock 文件"""
    project_root = Path(__file__).parent.parent
    
    print("\n" + "=" * 60)
    print("🔒 生成 uv.lock 文件")
    print("=" * 60)
    
    if not check_uv_installed():
        print("\n⚠️  uv 未安装或不在 PATH 中")
        response = input("\n是否尝试安装 uv? (y/n): ").strip().lower()
        
        if response == 'y':
            if not install_uv():
                print("\n❌ 无法自动安装，请手动安装:")
                print("   1. 访问: https://docs.astral.sh/uv/getting-started/installation/")
                print("   2. 或运行: pip install --user uv")
                return False
        else:
            print("跳过安装")
            return False
    
    print(f"\n📁 项目目录: {project_root}")
    print("\n正在生成 uv.lock ...")
    
    try:
        result = subprocess.run(
            ["uv", "lock"],
            cwd=project_root,
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            lock_file = project_root / "uv.lock"
            if lock_file.exists():
                size_kb = lock_file.stat().st_size / 1024
                print(f"\n✅ uv.lock 生成成功!")
                print(f"   文件大小: {size_kb:.2f} KB")
                print(f"   文件路径: {lock_file}")
                
                with open(lock_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    pkg_count = sum(1 for line in lines if 'name =' in line and line.strip().startswith('name'))
                    print(f"   包数量: ~{pkg_count} 个依赖")
                
                return True
            else:
                print("⚠️  命令成功但未找到 lock 文件")
                print(result.stdout)
                return False
        else:
            print(f"❌ 生成失败:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "🔐" * 30)
    print("LangGraph Agent - UV Lock 文件生成器")
    print("🔐" * 30)
    
    success = generate_lock_file()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 完成! 现在使用 uv 管理项目依赖:\n")
        print("   安装依赖:     uv sync")
        print("   运行项目:     uv run python main.py")
        print("   添加依赖:     uv add <package>")
        print("   更新依赖:     uv lock --upgrade-package <package>")
        return 0
    else:
        print("❌ 失败! 备选方案:\n")
        print("   使用 pip:      pip install -e .")
        print("   手动创建:     编辑 uv.lock 文件")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
