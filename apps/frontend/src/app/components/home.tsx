export default function Home() {
    return (
      <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <header className="row-start-1 w-full flex justify-end gap-4 items-center">
          <a href="/auth/login?screen_hint=signup" className="px-4 py-2 text-sm rounded-full bg-foreground text-background hover:bg-[#383838] dark:hover:bg-[#ccc]">
            Sign Up
          </a>
          <a href="/auth/login" className="px-4 py-2 text-sm rounded-full bg-foreground text-background hover:bg-[#383838] dark:hover:bg-[#ccc]">
            Login
          </a>
        </header>
  
        <main className="flex flex-col gap-8 row-start-2 items-center text-center max-w-3xl mx-auto">
          <h1 className="text-4xl sm:text-5xl font-bold">
            First Responders Management System
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Streamline emergency response operations with our comprehensive management platform
          </p>
  
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full mt-8">
            <div className="p-6 rounded-lg border border-black/[.08] dark:border-white/[.145]">
          <h3 className="font-bold mb-2">Real-time Dispatch</h3>
          <p className="text-sm">Coordinate emergency responses efficiently</p>
            </div>
            <div className="p-6 rounded-lg border border-black/[.08] dark:border-white/[.145]">
          <h3 className="font-bold mb-2">Resource Management</h3>
          <p className="text-sm">Track and allocate resources effectively</p>
            </div>
            <div className="p-6 rounded-lg border border-black/[.08] dark:border-white/[.145]">
          <h3 className="font-bold mb-2">Analytics</h3>
          <p className="text-sm">Data-driven insights for better decision making</p>
            </div>
          </div>
  
          <div className="flex gap-4 items-center flex-col sm:flex-row mt-8">
            <a
          className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-6 sm:px-8"
          href="#demo"
            >
          Request Demo
            </a>
            <a
          className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-6 sm:px-8"
          href="#learn-more"
            >
          Learn More
            </a>
          </div>
        </main>
      </div>
    );
  }
  