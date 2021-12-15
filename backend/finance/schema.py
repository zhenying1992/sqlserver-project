from dataclasses import dataclass


@dataclass
class Cpu:
    name: str
    percent: int  # 使用的百分比
    core: int  # 核心数
    speed: int  # 时钟频率


@dataclass
class Memory:
    total: int
    free: int
    percent: int
    swap_total: int
    swap_free: int


@dataclass
class Disk:
    name: str
    total: int  # 总容量
    use: int  # 使用量
    free: int  # 空闲量
    percent: int  # 使用百分比


@dataclass
class Sys:
    process: int  # 进程数量
    uptime: str  # 启动时间
