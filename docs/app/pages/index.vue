<script setup lang="ts">
import { useAsciiEye } from '#imports'

const title = 'GUILT'

useSeoMeta({
  titleTemplate: '',
  title,
  ogTitle: title,
})

definePageMeta({
  colorMode: 'dark'
})

const eyeAsciiArt = useAsciiEye()

interface Feature {
  title: string
  description: string
}

const features: Feature[] = [
  {
    title: "Track your carbon emissions",
    description: "GUILT automatically collates data from your HPC jobs ready for later analysis."
  },
  {
    title: "Use everywhere",
    description: "You can install GUILT on any SLURM enabled system, no admin privileges required."
  },
  {
    title: "Report generation",
    description: "Generate detailed reports on your carbon emissions and energy usage with a single command."
  },
  {
    title: "Visualisation",
    description: "Create adhoc graphs and charts to visualise your data directly in the terminal."
  },
  {
    title: "Open Source",
    description: "GUILT is free and open source software, available for anyone to use and contribute to."
  },
  {
    title: "Backfill historical data",
    description: "Easily backfill data from previous HPC jobs to get a complete picture of your carbon emissions."
  }
]
</script>

<template>
  <main>
    <section class="px-4 py-8">
      <div class="overflow-hidden font-extrabold text-neutral-400">
        <pre class="leading-none whitespace-pre w-fit mx-auto text-lg">{{ eyeAsciiArt }}</pre>
      </div>

      <div class="h-8" />

      <div class="grid justify-center items-center font-extrabold mx-auto">
        <div class="row-start-1 col-start-1 hidden lg:flex justify-around items-center">
          <span v-for="letter in 'GUILT'" :key="letter" class="text-8xl text-red-900 inline-block">{{ letter }}</span>
        </div>

        <h1 class="row-start-1 col-start-1 text-5xl text-center text-red-700 lg:text-neutral-200 z-10 outlined-black">
          GREEN USAGE IMPACT LOGGING TOOL
        </h1>

        <p class="row-start-2 col-start-1 text-center text-neutral-400">CARBON EMISSIONS TRACKING FOR SLURM</p>
      </div>
    </section>

    <UContainer>
      <hr class="border-neutral-800" />

      <div class="flex justify-center">
        <ULink to="/getting-started" class="text-red-500 text-lg">Visit Documentation Here</ULink>
      </div>

      <hr class="border-neutral-800" />

      <p class="text-justify my-4">For those who use High-Performance Computing systems, the environmental cost of their work is often overlooked. With no built-in tools for measuring or displaying carbon emissions, users are left in the dark about their energy consumption and its impact on the climate. GUILT is a CLI that wraps around the SLURM workload manager to provide users with data analytics about their carbon emissions. This project forms part of the STFC Scientific Computing Department Energy Efficiency Team strategy to transition the department towards net zero.</p>

      <hr class="border-neutral-800" />

      <section class="not-prose grid grid-cols-2 gap-4 my-4">
        <article v-for="{ title, description } in features" :key="title">
          <h2 class="text-md text-neutral-200 font-bold mb-2">{{ title.toUpperCase() }}</h2>
          <p class="text-sm text-neutral-400">{{ description }}</p>
        </article>
      </section>
    </UContainer>
  </main>
</template>